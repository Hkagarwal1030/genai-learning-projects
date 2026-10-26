# Task 3 Frontend - React Chat Interface

This folder contains the React and Vite frontend for the Task 3 context-aware
AI assistant. It provides the browser chat interface and sends chat requests to
the Flask API in the parent Task 3 folder.

For backend setup, Groq configuration, and details of the full application,
see the [Task 3 README](../README.md).

## Screenshot

![Task 3 React chat interface showing a Markdown-formatted assistant response](../ScreenshotReact-Markdown.png)

## Requirements

- Node.js and npm.
- The Flask backend from the parent Task 3 project.
- A Groq API key configured for the backend. The frontend does not need or
  store the API key.

## Install dependencies

Open PowerShell and change to the frontend folder:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2\Task 3\frontend"
```

Install the exact package versions from `package-lock.json`:

```powershell
npm ci
```

## Run the development app

The browser frontend and Flask backend run as separate processes. First, open
a terminal in the parent Task 3 folder and start the backend:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2\Task 3"
uv run python server.py
```

Leave that terminal running. In a second terminal, start Vite:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 2\Task 3\frontend"
npm run dev
```

Open the local URL printed by Vite, typically `http://localhost:5173`. Keep
both servers running while using the chat.

During development, [vite.config.js](./vite.config.js) proxies requests to
`/api` to the Flask server at `http://127.0.0.1:5000`. This lets the frontend
use a relative API URL without configuring a separate API host.

## Use the chat

- Enter a question in the message box and press **Enter** or click **Send**.
- Press **Shift+Enter** to add a newline without sending.
- While a request is running, the interface shows a thinking state and disables
  the input controls.
- The conversation scrolls to the latest message automatically.
- Assistant answers support Markdown and GitHub-flavored Markdown, including
  lists and tables.
- Links in assistant answers open in a new browser tab.
- Request errors are shown in the conversation.

The frontend keeps the current messages and conversation ID in React state.
Reloading the page resets the frontend state and starts a new conversation.
The Flask server keeps conversation history in memory and clears it when that
server is restarted.

## How the frontend works

1. `src/main.jsx` mounts the React `App` component into the page element in
   `index.html`.
2. `src/App.jsx` maintains the message list, input value, loading status,
   detected intent, and conversation ID.
3. When a question is submitted, the app sends a JSON `POST` request to
   `/api/chat`, including the message and current conversation ID.
4. The Flask backend returns a conversation ID, detected intent, and answer.
   The frontend stores the ID for follow-up questions and displays the answer.
5. Assistant content is rendered with `react-markdown` and `remark-gfm`.
6. `src/App.css` and `src/index.css` provide the responsive chat layout and
   styles.

## Main files

- `src/App.jsx` - Chat UI, React state, keyboard handling, API request, and
  response rendering.
- `src/App.css` - Chat layout, message styles, Markdown presentation, and
  responsive styling.
- `src/index.css` - Global styles.
- `src/main.jsx` - React application entry point.
- `index.html` - Vite HTML page and React mount point.
- `vite.config.js` - React plugin and development API proxy.
- `package.json` - Dependencies and development scripts.
- `package-lock.json` - Locked npm dependency versions.
- `public/` and `src/assets/` - Static and imported frontend assets.

## Available commands

Run these commands from this `frontend` directory:

```powershell
npm run dev
npm run lint
npm run build
npm run preview
```

- `npm run dev` starts the Vite development server.
- `npm run lint` checks frontend source with Oxlint.
- `npm run build` creates an optimized production build in `dist/`.
- `npm run preview` serves the production build locally. The Flask backend
  must also be available for chat requests.

## Troubleshooting

### The chat page loads but sending a question fails

Make sure the Flask backend is running at `http://127.0.0.1:5000`. Check the
backend terminal for errors and confirm the Groq API key is configured as
described in the [parent Task 3 README](../README.md).

### The browser cannot load the Vite page

Confirm `npm run dev` is still running and open the exact local URL printed in
the terminal.

### `npm` or `node` is not recognized

Install Node.js with npm, open a new terminal, and retry the command.

### A package cannot be found

From this folder, reinstall the locked dependencies:

```powershell
npm ci
```

### The displayed page does not reflect recent changes

Check the Vite terminal for build errors and reload the page. Restart the
development server if necessary.

## Security note

The browser sends prompts to the local Flask API; the Flask backend sends the
prompt and relevant conversation context to Groq. Do not enter passwords,
credentials, API keys, or other sensitive information into the chat. Never
place the Groq API key in frontend source code or browser-exposed environment
variables.
