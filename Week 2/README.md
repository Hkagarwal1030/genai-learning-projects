# Week 2 - AI Chatbot Projects

This folder contains three related chatbot tasks, a copy of Task 1, and a
standalone terminal chatbot. The projects use Python and the Groq API; Task 3
also includes a React web interface.

Each task is a separate project with its own dependencies and README. Start
with the task-specific README before installing packages or launching an app.

## Projects at a glance

| Folder or file | What it contains | How to get started |
| --- | --- | --- |
| [`Task 1/`](./Task%201/) | Tkinter desktop chatbot using the Groq API. | Read [`Task 1/README.md`](./Task%201/README.md). |
| [`Task 2/`](./Task%202/) | Context-aware Python chatbot with a Tkinter interface and a terminal version. | Read [`Task 2/README.md`](./Task%202/README.md). |
| [`Task 3/`](./Task%203/) | Context-aware chatbot with a React/Flask web app and an optional Tkinter desktop app. | Read [`Task 3/README.md`](./Task%203/README.md). |
| [`bot.py`](./bot.py) | Standalone command-line chatbot. | See [Standalone `bot.py`](#standalone-botpy) below. |
| `.env` | Shared Groq configuration file used by the task projects. | See [Shared configuration](#shared-configuration). |

## Requirements

Requirements differ slightly between the projects:

- Python 3.11 or newer is used by the projects that include a `.python-version`
  file.
- A Groq account and API key are needed to send prompts to the Groq API.
- `uv` is used by Task 1 and Task 3 to install their Python dependencies.
- Node.js and npm are additionally required for Task 3's React frontend.
- Tkinter is needed for the desktop interfaces. It is included with most
  standard Windows Python installations.

Use a separate virtual environment for each task. Do not assume that installing
packages for one task installs them for the others.

## Shared configuration

The `.env` in this Week 2 folder is the intended shared configuration file for
Task 1, Task 2, and Task 3. Add the following settings to it:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

- `GROQ_API_KEY` is required. Replace the example value with your own key.
- `GROQ_MODEL` is optional for Task 1, Task 2, and Task 3. Those projects
  default to `openai/gpt-oss-120b` when it is not set.
- `bot.py` uses the fixed model `openai/gpt-oss-20b` instead of `GROQ_MODEL`.

Keep the API key private. Never paste it into source files, screenshots, chat
messages, or public repositories. Do not commit `.env` files containing
credentials. If a key is exposed, revoke it with Groq and create a replacement.

Task 2 and Task 3 also currently contain task-local `.env` files, but their
assistant modules explicitly load the shared `Week 2\.env` file. Use the
Week 2-level file as the source of configuration.

### Note about `bot.py`

`bot.py` is located directly inside `Week 2`, unlike the assistant modules
inside the task subfolders. Its current dotenv path points one directory above
Week 2 rather than to this folder's `.env`. As a result, the shared key in
`Week 2\.env` may not be loaded when you run this standalone script. Set
`GROQ_API_KEY` in the process environment before running it, or update its
dotenv path to point to the Week 2 folder. The task applications load the
shared file using their own paths.

## Running a project

### Task 1 - desktop chatbot

Open PowerShell and run:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2\Task 1"
uv sync
uv run python Chat-bot.py
```

The Tkinter window lets you submit questions and displays the chat history.
For package details and troubleshooting, see [`Task 1/README.md`](./Task%201/README.md).

### Task 1 copy

This folder is a separate copy of Task 1 and contains its own Python project
files. Treat it as an independent project: open its directory and follow
[`Task 1 copy/README.md`](./Task%201%20copy/README.md) rather than reusing
Task 1's virtual environment.

### Task 2 - context-aware assistant

Open PowerShell and run:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2\Task 2"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install groq python-dotenv
python chat_app.py
```

This starts the graphical app. To use the terminal chatbot instead, run:

```powershell
python context_assistant.py
```

Type `exit` in the terminal version to quit. See
[`Task 2/README.md`](./Task%202/README.md) for setup details and interface
instructions.

### Task 3 - web or desktop app

Task 3 needs separate terminals for the Flask backend and React frontend.

Install the Python backend dependencies:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2\Task 3"
uv sync
```

Install the frontend dependencies:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2\Task 3\frontend"
npm ci
```

Start the Flask backend in one terminal:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2\Task 3"
uv run python server.py
```

Start the React development server in a second terminal:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2\Task 3\frontend"
npm run dev
```

Open the local URL printed by Vite in a browser. Keep both servers running;
Vite proxies `/api` requests to Flask. To use Task 3's optional Tkinter app
instead, run `uv run python chat_app.py` from the Task 3 folder. See
[`Task 3/README.md`](./Task%203/README.md) for API details, screenshots, and
troubleshooting.

## Standalone `bot.py`

`bot.py` is an interactive command-line chatbot. It reads messages from the
terminal, recognizes a few basic intents (greeting and profile help), uses
recent messages as conversation history, and sends requests to Groq.

After configuring `GROQ_API_KEY` for this script (see the
[dotenv-path note](#note-about-botpy)), launch it with Python:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2"
python bot.py
```

Type a question at the `You:` prompt. Type `quit` to exit.

## Conversation and privacy notes

- Task 2 and Task 3 keep conversation history in memory while running. Their
  README files explain when that history is reset and how it is sent as model
  context.
- The Task 3 Flask server stores conversations in process memory, so restarting
  the server clears them.
- User prompts and relevant conversation history are sent to Groq to generate
  answers. Avoid entering passwords, credentials, or sensitive personal data.
- API use may be subject to provider rate limits or charges.

## Troubleshooting

### The API key is reported missing

Confirm `GROQ_API_KEY` is present and non-empty in `Week 2\.env`. For the
standalone `bot.py`, also account for its different dotenv path as described
above.

### A model is not found or access is denied

Check that the model is available to your Groq account. Task 1, Task 2, and
Task 3 default to `openai/gpt-oss-120b`; `bot.py` uses
`openai/gpt-oss-20b`.

### Python packages cannot be imported

Check that you installed dependencies in the virtual environment for the
specific task you are running. Follow that task's README and select the same
Python environment in VS Code.

### The Task 3 page cannot contact the assistant

Make sure both the Flask backend and Vite frontend are running. The frontend
uses Vite's `/api` proxy to reach Flask.
