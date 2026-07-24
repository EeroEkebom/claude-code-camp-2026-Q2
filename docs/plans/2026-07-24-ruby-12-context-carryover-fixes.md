# Ruby 12_context Carryover Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix two things that were dropped when `week1_baseline/ruby/11_tui` was carried forward into `week1_baseline/ruby/12_context`, both found by diffing the two step folders and confirming with reproduction scripts (not just guessed from the diff).

**Architecture:** No new abstractions — restore functionality that step 12's own new features (token tracking / compaction, and the config-driven system prompt) silently depend on but don't fully provide. Both fixes are localized: one method in `Agent`, one method + one bundled file in `Config`.

**Tech Stack:** Ruby, no test framework in this repo (confirmed: no rspec/minitest anywhere under `ruby/12_context`) — verification uses one-off scripts under `examples/`, matching the pattern already used by `docs/plans/python_port/00_config`.

## Global Constraints

- This is a teaching repo with no test suite. Every verification step below is a plain `ruby` script run with `bundle exec`, not `rspec`/`minitest`.
- Do not touch `week1_baseline/ruby/11_tui` — it stays as-is; only `12_context` changes.
- Preserve step 12's existing public method signatures (`Agent#run`, `Config#system_prompt`, etc.) — these fixes are internal-only.
- After code changes, re-run the full step 12 demo (`ruby examples/example.rb`, requires the local CircleMUD on `localhost:4000` and a real `ANTHROPIC_API_KEY` in `.boukensha/.env`, both already configured in this environment) to confirm nothing regressed for the Anthropic path.

---

## Background — what's actually broken

Diffing `ruby/11_tui` against `ruby/12_context` shows most differences are step 12's intentional new feature (token tracking, `/compact`, reasoning logging — all consistent and well-commented). Two things are not intentional simplifications, they're gaps:

### Gap 1 — cross-provider usage normalization was deleted, but step 12 now depends on it

`11_tui/lib/boukensha/agent.rb` had a `normalized_usage(response)` helper that handled three raw-HTTP-response shapes:
- Anthropic / OpenAI: top-level `"usage"` key with `"input_tokens"`/`"output_tokens"`.
- Gemini: top-level `"usageMetadata"` key with `"promptTokenCount"`/`"candidatesTokenCount"`.
- Ollama (local): top-level `"prompt_eval_count"`/`"eval_count"` keys, no wrapper.

In step 11 this only fed display/logging. In step 12 (`12_context/lib/boukensha/agent.rb:88-92`), `record_usage` reads `response["usage"]` **directly**, with no fallback, and feeds it into the new context-tracking math:

```ruby
def record_usage(response)
  usage = response["usage"] || {}
  @context.add_turn_tokens(usage["input_tokens"], usage["output_tokens"])
  @context.update_tokens(usage["input_tokens"].to_i)
end
```

For Gemini and Ollama, `response["usage"]` is always `nil` (they don't use that key), so `usage` is always `{}`, so every turn silently records **zero tokens used**. Concretely: `Context#needs_compaction?` (`12_context/lib/boukensha/context.rb:57-59`) computes `usage_fraction = current_tokens.to_f / context_window`, which stays `0.0` forever — **auto-compaction, the flagship feature of step 12, never triggers for Gemini or Ollama sessions.** It also silently corrupts the token/cost stats written to the session `.jsonl` log and shown in `log_viz` (`week1_baseline/log_viz/lib/log_viz/session.rb:100-107` reads `usage["input_tokens"]`/`usage["output_tokens"]` from the same log events).

This doesn't show up in casual testing because this project's `settings.yaml` defaults to `provider: anthropic`, which happens to use the `"usage"` key already — the bug is fully silent (no exception, no error message) and only affects Gemini/Ollama backends.

### Gap 2 — no bundled default system prompt

`11_tui/lib/boukensha/tasks/base.rb` fell back to a prompt shipped with the step (`Config::PROMPTS_DIR`, pointing at `11_tui/prompts/system.md`) when no user-level prompt override existed. Step 12 deleted the whole `Tasks::` layer and replaced it with `Config#system_prompt` (`12_context/lib/boukensha/config.rb:120-132`), which only looks in the **user's own** `.boukensha/prompts/` directory — there is no bundled fallback file anywhere in `12_context`, and no `12_context/prompts/` directory at all:

```ruby
def load_system_prompt
  if dig(:tasks, :player, :prompt_override, :system) == true
    task_file = File.join(@dir, "prompts", "player", "system.md")
    return File.read(task_file).strip if File.exist?(task_file)
  end

  system_file = File.join(@dir, "prompts", "system.md")
  File.exist?(system_file) ? File.read(system_file).strip : nil
end
```

This project's own `.boukensha/settings.yaml` happens to set `prompt_override.system: true` and ship `.boukensha/prompts/player/system.md`, so it's currently masked — but a fresh `.boukensha` (default settings, no custom prompts) gets `system_prompt == nil`, i.e. the agent silently runs with **no system prompt at all**. (Note: step 11's bundled fallback was itself already broken when running from an *installed gem* — `boukensha.gemspec:17` never packages `prompts/**` — so this only fully worked via `bundle exec` inside the repo checkout. Step 12 loses that too.)

---

## Task 1: Restore cross-provider usage normalization

**Files:**
- Modify: `week1_baseline/ruby/12_context/lib/boukensha/agent.rb:61,88-92,114,157`
- Test: `week1_baseline/ruby/12_context/examples/verify_usage_normalization.rb` (new, one-off — delete after manual verification, don't commit it)

**Interfaces:**
- Consumes: `Boukensha::Context#add_turn_tokens(input, output)`, `#update_tokens(n)` (unchanged, already nil-safe via `.to_i`)
- Produces: `Agent#normalized_usage(response)` → always returns a `Hash` with `"input_tokens"`/`"output_tokens"` keys (possibly `nil` values, never raises), used everywhere `agent.rb` currently reads `response["usage"]` raw.

- [ ] **Step 1: Write the reproduction script (fails against current code)**

Create `week1_baseline/ruby/12_context/examples/verify_usage_normalization.rb`:

```ruby
#!/usr/bin/env ruby
# frozen_string_literal: true
#
# One-off reproduction/verification script (no test framework in this repo).
# Builds a minimal Agent + Context and feeds it fake raw provider responses,
# shaped exactly like Gemini's and Ollama's real HTTP responses, to check
# that token tracking is populated regardless of backend.

$LOAD_PATH.unshift File.expand_path("../lib", __dir__)
require "boukensha"

def check(name, response, ctx)
  agent = Boukensha::Agent.allocate
  agent.instance_variable_set(:@context, ctx)
  agent.send(:record_usage, response)
  input  = ctx.instance_variable_get(:@turn_tokens)
  total  = ctx.current_tokens
  status = (input > 0 && total > 0) ? "OK" : "BROKEN (turn_tokens=#{input}, current_tokens=#{total})"
  puts "#{name}: #{status}"
end

gemini_response = {
  "usageMetadata" => { "promptTokenCount" => 120, "candidatesTokenCount" => 30, "totalTokenCount" => 150 }
}
ollama_response = {
  "prompt_eval_count" => 80, "eval_count" => 20
}
anthropic_response = {
  "usage" => { "input_tokens" => 100, "output_tokens" => 25 }
}

check("anthropic", anthropic_response, Boukensha::Context.new(system: nil))
check("gemini",    gemini_response,    Boukensha::Context.new(system: nil))
check("ollama",    ollama_response,    Boukensha::Context.new(system: nil))
```

- [ ] **Step 2: Run it to confirm gemini/ollama are broken, anthropic is fine**

Run: `cd week1_baseline/ruby/12_context && bundle exec ruby examples/verify_usage_normalization.rb`

Expected (current, broken):
```
anthropic: OK
gemini: BROKEN (turn_tokens=0, current_tokens=0)
ollama: BROKEN (turn_tokens=0, current_tokens=0)
```

- [ ] **Step 3: Add the normalization helper and use it everywhere `response["usage"]` is read raw**

In `week1_baseline/ruby/12_context/lib/boukensha/agent.rb`, replace the `record_usage` method (currently lines 88-92):

```ruby
    # Add this call's input+output to the cumulative turn total (the spend
    # budget) and refresh the known context size from input_tokens (compaction
    # pressure). The trigger is evaluated on pre-wrap-up spend; the reported
    # total includes the wind-down call too.
    def record_usage(response)
      usage = normalized_usage(response)
      @context.add_turn_tokens(usage["input_tokens"], usage["output_tokens"])
      @context.update_tokens(usage["input_tokens"].to_i)
    end

    # Providers report usage under different raw-response shapes:
    #   Anthropic / OpenAI — top-level "usage": {"input_tokens", "output_tokens"}
    #   Gemini             — top-level "usageMetadata": {"promptTokenCount", "candidatesTokenCount"}
    #   Ollama (local)     — top-level "prompt_eval_count" / "eval_count", no wrapper
    # Normalize all of these to a common {"input_tokens" => n, "output_tokens" => n}
    # shape so record_usage's math and the logger's persisted usage chip (which
    # log_viz reads back out) work identically for every backend.
    def normalized_usage(response)
      return response["usage"] if response["usage"]

      if (meta = response["usageMetadata"])
        return {
          "input_tokens"  => meta["promptTokenCount"],
          "output_tokens" => meta["candidatesTokenCount"]
        }
      end

      if response.key?("prompt_eval_count") || response.key?("eval_count")
        return {
          "input_tokens"  => response["prompt_eval_count"],
          "output_tokens" => response["eval_count"]
        }
      end

      {}
    end
```

Then update the three remaining raw reads to go through the same helper — in the same file:

Line 61 (inside `run`):
```ruby
          @logger.response(text: text, usage: response["usage"], stop_reason: parsed[:stop_reason])
```
becomes:
```ruby
          @logger.response(text: text, usage: normalized_usage(response), stop_reason: parsed[:stop_reason])
```

Line 114 (inside `wrap_up`):
```ruby
      @logger.response(text: text, usage: response["usage"], stop_reason: parsed_wrap[:stop_reason])
```
becomes:
```ruby
      @logger.response(text: text, usage: normalized_usage(response), stop_reason: parsed_wrap[:stop_reason])
```

Line 157 (inside `handle_tool_calls`):
```ruby
      @logger.response(text: "(tool use — #{tool_calls.size} call#{'s' if tool_calls.size != 1})", usage: response["usage"], stop_reason: "tool_use")
```
becomes:
```ruby
      @logger.response(text: "(tool use — #{tool_calls.size} call#{'s' if tool_calls.size != 1})", usage: normalized_usage(response), stop_reason: "tool_use")
```

- [ ] **Step 4: Re-run the reproduction script to confirm it now passes**

Run: `bundle exec ruby examples/verify_usage_normalization.rb`

Expected:
```
anthropic: OK
gemini: OK
ollama: OK
```

- [ ] **Step 5: Delete the one-off script (not part of the shipped lesson)**

Run: `rm week1_baseline/ruby/12_context/examples/verify_usage_normalization.rb`

- [ ] **Step 6: Smoke-test the real Anthropic path still works end-to-end**

Run: `cd week1_baseline/ruby/12_context && bundle exec ruby examples/example.rb`
Expected: same as before this change — `Config: ...` / `API key set? true` line, exit code 0, no exceptions. (The MUD server on `localhost:4000` must be running; it already is in this environment.)

- [ ] **Step 7: Commit**

```bash
git add week1_baseline/ruby/12_context/lib/boukensha/agent.rb
git commit -m "$(cat <<'EOF'
Restore cross-provider usage normalization in step 12's Agent

record_usage read response["usage"] directly, which only exists for
Anthropic/OpenAI raw responses. Gemini (usageMetadata) and Ollama
(prompt_eval_count/eval_count) silently recorded zero tokens per turn,
so needs_compaction? never tripped and session logs/log_viz showed
zero cost for those backends. Restores the normalized_usage helper
that existed in 11_tui (there it only fed logging; here it also feeds
the new context-tracking math, so it needs the same key names
record_usage expects).
EOF
)"
```

---

## Task 2: Restore a bundled default system prompt

**Files:**
- Create: `week1_baseline/ruby/12_context/prompts/system.md`
- Modify: `week1_baseline/ruby/12_context/lib/boukensha/config.rb:10-19` (add `PROMPTS_DIR` constant, thread it through), `:120-132` (`load_system_prompt` fallback)
- Test: `week1_baseline/ruby/12_context/examples/verify_default_prompt.rb` (new, one-off — delete after manual verification, don't commit it)

**Interfaces:**
- Consumes: nothing new
- Produces: `Config::PROMPTS_DIR` (constant, absolute path to `12_context/prompts`), `Config#system_prompt` now returns the bundled default text instead of `nil` when the user hasn't configured any prompt override.

- [ ] **Step 1: Write the reproduction script (fails against current code)**

Create `week1_baseline/ruby/12_context/examples/verify_default_prompt.rb`:

```ruby
#!/usr/bin/env ruby
# frozen_string_literal: true
#
# One-off reproduction/verification script. Points BOUKENSHA_DIR at a bare
# temp config dir (settings.yaml only, no prompts/, no prompt_override) to
# simulate a fresh install, then checks Config#system_prompt isn't nil.

require "tmpdir"
require "fileutils"

Dir.mktmpdir do |dir|
  File.write(File.join(dir, "settings.yaml"), <<~YAML)
    tasks:
      player:
        provider: anthropic
        model: claude-haiku-4-5
  YAML

  ENV["BOUKENSHA_DIR"] = dir
  $LOAD_PATH.unshift File.expand_path("../lib", __dir__)
  require "boukensha"

  cfg = Boukensha::Config.new
  if cfg.system_prompt.nil?
    puts "BROKEN: system_prompt is nil for a fresh config dir with no custom prompts"
  else
    puts "OK: system_prompt = #{cfg.system_prompt.inspect}"
  end
end
```

- [ ] **Step 2: Run it to confirm the gap**

Run: `cd week1_baseline/ruby/12_context && bundle exec ruby examples/verify_default_prompt.rb`

Expected (current, broken): `BROKEN: system_prompt is nil for a fresh config dir with no custom prompts`

- [ ] **Step 3: Add the bundled default prompt file**

Create `week1_baseline/ruby/12_context/prompts/system.md` with the same content step 11 shipped:

```markdown
You are Boukensha, an autonomous player exploring a CircleMUD world.

Use available tools to observe the world, act deliberately, and explain only what matters for the current turn.
```

- [ ] **Step 4: Add `PROMPTS_DIR` and wire the fallback into `Config`**

In `week1_baseline/ruby/12_context/lib/boukensha/config.rb`, add the constant next to `DEFAULT_DIR` (currently line 10):

```ruby
    DEFAULT_DIR = File.join(Dir.home, ".boukensha").freeze

    # Default prompt shipped alongside this step, used when the user hasn't
    # configured their own (matches the behavior 11_tui had via Tasks::Base).
    PROMPTS_DIR = File.expand_path("../../../prompts", __dir__).freeze
```

Then change `load_system_prompt` (currently lines 120-132) to fall back to it as a last resort:

```ruby
    # Resolves the system prompt. When the player task opts into a prompt
    # override (tasks.player.prompt_override.system: true), the task-scoped
    # file prompts/player/system.md wins; otherwise the flat prompts/system.md
    # in the user's config dir is used; if neither exists, fall back to the
    # default prompt bundled with this step.
    def load_system_prompt
      if dig(:tasks, :player, :prompt_override, :system) == true
        task_file = File.join(@dir, "prompts", "player", "system.md")
        return File.read(task_file).strip if File.exist?(task_file)
      end

      system_file = File.join(@dir, "prompts", "system.md")
      return File.read(system_file).strip if File.exist?(system_file)

      bundled_file = File.join(PROMPTS_DIR, "system.md")
      File.exist?(bundled_file) ? File.read(bundled_file).strip : nil
    end
```

- [ ] **Step 5: Package `prompts/**` into the gemspec (the pre-existing gap noted above — fix it here since it's a one-line addition and Task 2 is pointless without it for installed-gem usage)**

In `week1_baseline/ruby/12_context/boukensha.gemspec`, change:
```ruby
  spec.files = Dir["lib/**/*.rb"] + ["bin/boukensha"]
```
to:
```ruby
  spec.files = Dir["lib/**/*.rb"] + Dir["prompts/**/*"] + ["bin/boukensha"]
```

- [ ] **Step 6: Re-run the reproduction script to confirm it now passes**

Run: `bundle exec ruby examples/verify_default_prompt.rb`

Expected: `OK: system_prompt = "You are Boukensha, an autonomous player exploring a CircleMUD world.\n\nUse available tools to observe the world, act deliberately, and explain only what matters for the current turn."`

- [ ] **Step 7: Delete the one-off script**

Run: `rm week1_baseline/ruby/12_context/examples/verify_default_prompt.rb`

- [ ] **Step 8: Smoke-test this project's real config still uses its own override, unaffected**

Run: `cd week1_baseline/ruby/12_context && bundle exec ruby -e '
$LOAD_PATH.unshift File.expand_path("lib")
require "boukensha"
puts Boukensha::Config.new.system_prompt
'`

Expected: prints the content of this project's `week1_baseline/.boukensha/prompts/player/system.md` (unchanged from before this task — confirms the existing override path still wins over the new bundled fallback).

- [ ] **Step 9: Commit**

```bash
git add week1_baseline/ruby/12_context/prompts/system.md \
        week1_baseline/ruby/12_context/lib/boukensha/config.rb \
        week1_baseline/ruby/12_context/boukensha.gemspec
git commit -m "$(cat <<'EOF'
Restore bundled default system prompt for step 12

Config#system_prompt returned nil for a fresh .boukensha with no
custom prompts/prompt_override configured — the Tasks::Base bundled
fallback that 11_tui had (Config::PROMPTS_DIR) was dropped along with
the rest of the Tasks:: layer. Ships 12_context/prompts/system.md and
a matching fallback in Config#load_system_prompt, and packages
prompts/** in the gemspec (11_tui never did, so it was already broken
for anyone using the installed gem rather than bundle exec).
EOF
)"
```

---

## Self-review notes

- **Spec coverage:** Both gaps identified in the Background section have a task. No other genuine regression was found after diffing every changed file between `11_tui` and `12_context` (`tasks`/`prompts` directory removal, `file_system.rb`'s `list_directory`/`search_files` being commented out, and all `agent.rb`/`repl.rb`/`context.rb` additions were confirmed intentional and consistent — see conversation history for the full diff walkthrough).
- **Scope not covered by this plan:** `12_context/examples/example.rb` is a byte-identical carryover of the step-10 MUD demo and never prints `Boukensha.run`'s return value, so running it produces no visible agent output beyond the `Config:`/`API key set?` lines. This is true of steps 9 through 12 identically (not a step-12-specific regression), so it's left out of this plan — flag separately if it should be fixed.
