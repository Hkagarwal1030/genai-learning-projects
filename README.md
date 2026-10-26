# GENAI Learning Projects

This workspace contains hands-on Python and generative-AI exercises organized
by week. The projects explore calling the Groq API, validating structured
data, building context-aware assistants, and creating desktop and web chat
interfaces.

## Contents

| Folder | Overview | Start here |
| --- | --- | --- |
| [`Week 1/`](./Week%201/) | Three introductory exercises: a Groq API call, local Pydantic validation, and LLM-generated structured profile data. | [`Week 1/README.md`](./Week%201/README.md) |
| [`Week 2/`](./Week%202/) | Groq chatbot projects, including Tkinter desktop apps, a context-aware assistant, and a React/Flask web app. | [`Week 2/README.md`](./Week%202/README.md) |
| [`.vscode/`](./.vscode/) | VS Code workspace settings. | Optional editor configuration. |

Each week and task is its own project. Read the relevant README before
installing packages or running a script; dependency and setup instructions
vary between exercises.

## Requirements

Requirements depend on the project you choose. In general, you may need:

- Python (use the version specified in a task's `.python-version` file, if
  present).
- Node.js and npm for the Week 2 Task 3 React frontend.
- `uv` or `pip` for installing Python dependencies, as described in the
  project's README.
- Tkinter for the desktop chatbot interfaces. It is included with most
  standard Windows Python installations.
- A Groq account and API key for tasks that make Groq API requests.

Use each task's own virtual environment rather than assuming dependencies
installed for one task are available to another.

## Getting started

1. Choose a project under [`Week 1/`](./Week%201/) or
   [`Week 2/`](./Week%202/).
2. Open that week's README, then follow the task-specific README linked from
   it.
3. Install the dependencies for that task.
4. Configure the API key in the location and format specified by the task.
5. Run the script or start the app using its documented command.

## API keys and privacy

Some tasks send prompts and conversation context to Groq. Configure API keys
as described by the relevant project and never paste them into source code,
screenshots, chat messages, or public repositories. Do not commit files
containing secrets. If a key is exposed, revoke it with the provider and
create a replacement.

Avoid sending passwords, credentials, or sensitive personal information to
the assistants. API requests may be subject to provider rate limits or
charges.

## Notes about configuration

- Week 1 API examples read `GROQ_API_KEY` from the process environment; see
  [`Week 1/README.md`](./Week%201/README.md) for PowerShell instructions.
- Week 2 task applications primarily use the shared `.env` file documented
  in [`Week 2/README.md`](./Week%202/README.md). The standalone Week 2
  `bot.py` has a different dotenv path, which is explained there.
