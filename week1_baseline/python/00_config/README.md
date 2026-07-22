# 00 · Configuration (Python port)

Python port of `week1_baseline/ruby/00_config`. See that lesson's README for
the full design rationale — this file only calls out where the Python port
differs.

We want to be able to manage all configuration from an external file, e.g.
`~/.boukensha/settings.toml`. A dedicated `Config` class handles it. As we add
configuration in each iteration we will keep updating the schema and class.
We can hardcode defaults but we should not hardcode configurable values.

Configuration is organised by **task** — a role in the agentic loop bound to
its own LLM. week1_baseline only drives a single `player` task (the main
loop); a more advanced loop will assign different LLMs to different tasks.

## Design Considerations

We want to use the standard library as much as possible, avoiding third-party
packages. The one necessary addition is `python-dotenv`, to load `.env`
files — the direct Python analog of Ruby's `dotenv` gem.

**Format difference from Ruby:** Ruby's stdlib ships a YAML parser, so the
Ruby lesson uses `settings.yaml`. Python's stdlib has no YAML parser but does
ship `tomllib` (read-only TOML, Python ≥3.11) — so the Python port uses
`settings.toml` instead of adding a third-party YAML dependency. Both files
live side by side in the same shared `.boukensha/` directory; Ruby reads
`settings.yaml`, Python reads `settings.toml`.

## Code Changes

| File | Purpose |
|------|---------|
| `boukensha/config.py` | `Config` class |
| `boukensha/tasks/base.py` | abstract `Base` (provider/model + prompt resolution) |
| `boukensha/tasks/player.py` | concrete `Player` (the main loop) |
| `boukensha/__init__.py` | top-level package exports |
| `prompts/system.md` | default system prompt shipped with the package |
| `examples/example.py` | runnable smoke test |

## Config directory resolution

Same as Ruby — the class looks for a `.boukensha/` directory in this order:

1. **`BOUKENSHA_DIR` env var**
2. **`~/.boukensha`** — the default location for a real install.

## Config directory structure

```
.boukensha/
  .env                 # credentials, e.g. LLM API keys (never committed)
  settings.toml        # all non-secret settings
  prompts/
    <task>/
      system.md        # per-task override for the default system prompt (optional)
```

## Tasks

`Base` is an abstract stateless class — no instances are created, everything
is a classmethod taking a `settings` dict. Concrete subclasses set
`task_name`. For now only `Player` exists.

```python
from boukensha import Config, Player

config = Config()
player_settings = config.tasks("player")

Player.provider(player_settings)
Player.system_prompt(
    player_settings,
    user_prompts_dir=config.user_prompts_dir,
    default_prompts_dir=Config.PROMPTS_DIR,
)
```

## System prompt resolution

Per task, `Player.system_prompt` is resolved in this order:

1. **`.boukensha/prompts/<task>/system.md`** — used when the task's
   `prompt_override.system` is `true` and the file exists.
2. **`prompts/system.md`** — the default system prompt shipped with the package.

## Configuration Schema

```toml
[tasks.player]
provider = "anthropic"       # provider name (string)
model = "claude-haiku-4-5"

[tasks.player.prompt_override]
system = true

[mud]
host = "localhost"
port = 4000
username = "dummy"
password = "helloworld"
```

## Run Example

```bash
uv run --project week1_baseline/python/00_config examples/example.py
# or:
./week1_baseline/python/bin/00_config
```

Expected output (values from your `.boukensha/`):

```
=== Boukensha Step 0: Configuration ===

Config dir:     /home/you/Sites/claude-code-camp-2026-Q2/week1_baseline/.boukensha
Tasks:          player

-- player task --
Provider:       anthropic
Model:          claude-haiku-4-5
Prompt override?True
System prompt:  You are a MUD player assistant. Use the tools available to y...

MUD host:       localhost:4000
MUD user:       dummy

API key set?    True

<Config dir=/home/you/Sites/claude-code-camp-2026-Q2/week1_baseline/.boukensha tasks=player>
```
