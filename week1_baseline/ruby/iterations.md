# What is goal for week 1?

We want to build a baseline agent that has all common components for building any kind of agent. Things it should include:
- a simple agentic loop
- a tool registry along with tools
- it should be able to handle multiple backends
- it should be able to produce some logs
- it should have an DSL so we can use the agent like an SDK
- it should have global binary execution so we can interact via the CLI
- we should have an optional CLI mode
- it should manage context and compact messages when reaching our set limits
- it should have its own configuration directory

Some other things we should have:
- log visualizer so we can better view logs in the browser

## What should the baseline agent be able to do?
It should be able to play the MUD albeit we will have to give it specific commands

## What will it not be able to do?
It will have poor perception since it will not have a way of managing memory, or decision making, or be token effective

## Technical Design Considerations:
- we will use REST APIs directly, this design choice is so we are understanding how simple it is to interact with Managed APIs and how much the vary
- some SDKs, even official ones, do not expose all features and so REST APIs will give full access to feature sets
- we are using Ruby but the end user can port it over to another language
- we must use the Ruby MudManager to interact with the MUD
- we should attempt to use the standard library (STDs) as much as possible and avoiding introducing third party libraries

### What should we not use?
- we should avoid using Agent SDKs since they already implement features we are implementing from scratch. They also might limit our ability to implement exactly what we need.
    - e.g. don't use OpenRouter, or don't use Amazon Strands or CoreAgent or LangChain
- we shouldn't be using the coding harness to drive the agent, since that is not purposed for our agent task.

## Explain Structure Approach
The 'ruby/' folder contains each step-by-step iteration for our agent.

### Considerations
- We will need to make some manual adjustments since the original code did not exist in a ruby sub-folder.
- AI affected the handwritten code so we will identify parts that should be rewritten but we may leave intact for not to disturb future layers.
- We can and will port the code to python, we will have to ensure the MudManager Ruby version works both with Ruby and Python.

## Student Completion Approaches:
As a student you have some flexibility in how you can get through this week.:
- You can exactly follow along and make the Ruby changes.
    - You can treat the Ruby implementation as your main implementation
- If you have no interest in the Python porting you can completely ignore those videos
- You can watch all the videos and then do a single port of the last Ruby iteration to your language of choice
- You don't have to port the Ruby but you will have to use it in your Week 2 when we implement extra capabilities

This is so you can:
- use the technical documentation and code reference to generate out code in your preferred language and coding standards.
- easily understand each part added without having to navigate git history.

## Baseline Mud Agent

The baseline MUD agent is a fully working MUD agent that can connect to a tbaMUD server, log in as a character, and control it through natural language.

**What the baseline gives you:**
- A persistent TCP session to the MUD server that stays connected across the agent's tool calls
    - technically the MudManager is persisting the connection
- Five interchangeable LLM backends (Anthropic, OpenAI, Gemini, Ollama, Ollama Cloud) behind one normalized request/response shape, configured per-task in 'settings.yaml'
    - Andrew implements multiple backends, the student can use a single backend or multiple backends, it's up to them
- MUD tools covering every core action: movement, combat, perception, inventory, magic and communication
    - MudManager implements specific actions, but there are actions missing, e.g. Thief commands, rest commands - The student needs to consider solving these at some point, in (a) end of Week 1 or (b) in Week 2.
- A standard tool library for file I/O and shell commands so the agent can also read/write local state. 
    - These tools are simply nearing the MudManager tools and likely need reworking which does not occur in Week 1.
- A multi-turn REPL so you can have a back-and-forth conversation with the agent while it plays
- Full conversation history carried across turns so the agents remembers what it has seen and done
    - This is the sessions log files, but consider we can't load previous conversations since we don't implement those features in the Agent.
- Coloured structured logging of every API call, tool dispatch and response
    - Technically there is a bit of colouring, but the web-browser logger provides more information.

**What it does not yet have** (to be added in later iterations)
- Long-term memory beyond the current conversation window
- A world model or map built from exploration
- Goal planning, tactical reasoning, or autonomous behaviour
- Character progression tracking or strategy

- For each of our steps often we will have a class for each e.g. Configuration will config, REPL will have repl.rb

### 0 Configuration

`Boukensha::Config` and ~/.boukensha directory stores all our configuration data including
secrets, prompts, logging (aka sessions) and settings file.

We have a env var called BOUKENSHA_DIR that lets override its default location which is in the
user's home directory.

We do use .dotenv standard for storing our secrets and we do need to include the dotenv library.

> If we are building an agent that can be deployed on multiple servers, a configuration directory
> seems appropriate. 

- the single source of truth for all settings. 
Loads `~/.boukensha/` by default (override with `BOUKENSHA_DIR`). 
Reads `.env` for secrets, `settings.yaml` for options, and `system.md` for the default system prompt.

### 1 The Struct Skeleton

Define `Boukensha::Tool`, `Boukensha::Message`, and `Boukensha::Context` as plain data containers.
No logic yet, just the shapes.

We are defining the main datastructure to pass around data.

### 2 The Tool Registry

`Boukensha.tool` DSL method that registers a name + block. Add `Boukensha.dispatch(name,args)` to call on(e?).
Runnable: register a fake tool and call it.

The Tool Registry is responsible for managing a data table of possible tools, and also dispatch tools when called. In other
words, it matches a prompt call to an appropriate tool.

> We did discover that at some point the AI regressed the implementation and Context is still responsible
> for managing tools which is not correct and the tools[] need to be moved to the Tool Registry.

### 3 The Prompt Builder

Since we are calling multiple platforms via direct REST API requests, we need to know exactly where their schema structure
resides. So we need to build those expected structures. 

We also need the prompt builder to normalize the responses into a single standard.

> We have to consider the thinking option models, some models have thinking turned on as default while others do not, some cannot turn off their thinking. There are other parameters we can finetune as well, but we didn't have much time exploring them in the videos.

### 4 The API Client

The API Client is simply a low-level http-server making a direct API call to the REST API.

> We ended up hardcoding the exact OpenSSL path, and this changes based on Windows, Mac or Linux, a third-party http-server like HTTPParty or Faraday would solve this but it will abstract more and make it harder to see the moving parts and we would have to take a library so we just fix the code for where we run it.

### 5 The Agent Loop

`Boukensha::Agent` - the core agentic loop. Calls the API, checks `stop_reason`, dispatches tool calls back into the registry, appends results to the context, and repeats until `end_turn` or `MAX_ITERATIONS` is hit. Adds `Boukensha::Errors` (`LoopError`, `ApiError`) and wires everything together in `Boukensha.run`.

Also brings the OpenAI, Gemini, and Ollama Cloud backends online alongside Anthropic and Ollama - each implements `parse_response` to convert its raw reply into one normalized `{stop_reason:, content:}` shape so `Agent` never has to know which provider it's talking to.

> So we mentioned earlier we need to normalize the responses in the prompt backend and so it occurs here I believe we implement that normalization within the prompt builder and their backends. 

### 6 The Logger

We create a logger which will record the logs of a session in ~/.boukensha/sessions/<date>-<session_id>.jsonl(og)

> We have a log_viz app which is a simple Sinatra app to visualize the sessions. We should really in the future port it to typeScript and have it realtime.

We make sure we store exactly which model, which provider and cost, trying to uplift as much information on each call for details reporting and also allowing us to mid conversation switch agents (despite lacking commands to due so in the CLI).

### 7 The Run DSL

Up to the point we have multiple classes we need to create instances of and it becomes a mess of code so we implement a single .run command to abstract away the complexity and give us a SDK like interface to our agent.

`Boukensha::RunDSL` - the object `self` becomes inside a `Boukensha.run { }` block. Exposes a single `tool` method so callers can register ad-hoc tools inline alongside the task, keeping the DSL surface small and the main `Boukensha.run` signature clean.

### 8 The REPL Loop

It lets us have an interactive loop for the terminal.

`Boukensha::Repl` - an interactive session that stays alive across turns. Reads user input, runs the agent, prints the reply, and loops back to the prompt. A single `Context` is shared across all turns so the agent sees full conversation history. Built-in commands: `/quiet`, `/loud`, `/clear` (wipe history, keep tools), `/exit`, `/quit`, `/help`. Adds `Boukensha::VERSION`.

### 9 Global Executable

Lets us call `boukensha` anywhere in terminal to start using our agent.

> Here a .boukensharc file gets introduced which allows us to set the configuration path and the current gem path for the boukensha binary to load and we end up having to carry that code in future steps. 

Packages everything as an installable gem so the `boukensha` command is available anywhere on the machine. Adds `boukensha.gemspec`, `bin/boukensha`, and `lib/boukensha_loader.rb`. The loader resolves which step folder to use in priority order: `BOUKENSHA_PATH` env var -> `~/.boukensharc` file -> bundled default. `BOUKENSHA_DEBUG=1` prints the resolved path on startup.

> stuff missing here.. it's on the 2nd(?) lecture vid around 25? mins in..

> this step was skipped for Python part, not sure if that was a bad idea but that happened

### 10 Standard Tool Library - MCP Host

We are implementing a mapping of tools for the agent from the Mud Manager. However when we went to port the code to Python, the Python app had no way of accessing the MudManager ruby version, so we ended up implementing MCP.

> the MCP implementation is a 2h video, and it's worth watching, but not doing, so I would recommend copying over the MudManager and the 10_standard_tool_library from omenking repo.

> We end up adding the MCP server within Mud Manager so it's a single gem.

> also due to major code changes here we end up having to carry forward code which makes the Ruby steps more involved. 

> ..

### 11 Terminal UI

TUI is just a nicer REPL, so it has advanced display features within terminal.
> We end up using Charm BubbleTea for the TUI in Ruby, AI thinks BubbleTea is not available for Python and so ends up using Texual. In honesty since we have the log_viz, we don't really need a TUI but in my original implementation I implemented log_viz later.

### 12 Context Management

There is no auto-compacting when you call an LLM directly - you're responsible for the context window. This step adds proper token tracking, visual warnings, and automatic compaction on top of the MCP-host tool model and TUI carried forward from steps 10-11.

> There should be settings exposed to increase the 600 e.g. 60,000 max token limit, as that is a very low amount but we never tested it in Week 1 but it probably can be adjusted.

> Lots of stuff here.. check the vid.. around 33:00..