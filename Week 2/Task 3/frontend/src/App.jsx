
import { useRef, useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I'm your context-aware AI assistant. Ask me a question to get started.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [intent, setIntent] = useState("");
  const [conversationId, setConversationId] = useState("");

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(event) {
    event?.preventDefault();

    const message = input.trim();
    if (!message || loading) return;

    setInput("");
    setMessages((previous) => [
      ...previous,
      { role: "user", content: message },
    ]);
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          conversation_id: conversationId,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Request failed.");
      }

      setConversationId(data.conversation_id);
      setIntent(data.intent);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "error",
          content: error.message || "Unable to contact the assistant.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="header">
        <div>
          <h1>AI Chat Assistant</h1>
          <p>Context-aware conversations powered by Groq</p>
        </div>
        <span className="status">
          {loading ? "Thinking..." : "Ready"}
        </span>
      </header>

      <section className="chat" aria-live="polite">
        {messages.map((message, index) => (
          <article
            key={index}
            className={`message ${message.role}`}
          >
            <div className="message-label">
              {message.role === "user"
                ? "You"
                : message.role === "error"
                ? "Error"
                : `Assistant${intent && index === messages.length - 1 ? ` · ${intent}` : ""}`}
            </div>

            {message.role === "assistant" ? (
              <div className="markdown">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    a: ({ children, ...props }) => (
                      <a
                        {...props}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {children}
                      </a>
                    ),
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            ) : (
              <div className="plain-message">{message.content}</div>
            )}
          </article>
        ))}

        {loading && (
          <div className="typing">Assistant is generating a response…</div>
        )}

        <div ref={bottomRef} />
      </section>

      <form className="composer" onSubmit={sendMessage}>
        <textarea
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => {
            if (
              event.key === "Enter" &&
              !event.shiftKey &&
              !event.nativeEvent.isComposing
            ) {
              event.preventDefault();
              sendMessage();
            }
          }}
          placeholder="Ask a question..."
          aria-label="Message"
          rows={2}
          disabled={loading}
        />

        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? "Wait..." : "Send"}
        </button>
      </form>

      <footer className="footer">
        Enter to send · Shift + Enter for a new line
      </footer>
    </main>
  );
}

export default App;
