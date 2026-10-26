
import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import scrolledtext, messagebox

from dotenv import load_dotenv
from groq import Groq, APIConnectionError, APIStatusError, RateLimitError

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to your .env file."
    )

client = Groq(api_key=API_KEY)
history = []


class AIChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chat Assistant")
        self.root.geometry("650x600")
        self.root.minsize(450, 400)
        self.root.configure(bg="#f3f4f6")

        header = tk.Frame(root, bg="#1e293b", pady=14)
        header.pack(fill="x")

        tk.Label(
            header,
            text="AI Chat Assistant",
            font=("Segoe UI", 17, "bold"),
            bg="#1e293b",
            fg="white",
        ).pack()

        tk.Label(
            header,
            text="Powered by GroqCloud",
            font=("Segoe UI", 9),
            bg="#1e293b",
            fg="#cbd5e1",
        ).pack()

        self.chat = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="white",
            fg="#111827",
            padx=12,
            pady=12,
            state="disabled",
            relief="flat",
        )
        self.chat.tag_config("user", foreground="#2563eb")
        self.chat.tag_config("assistant", foreground="#047857")
        self.chat.tag_config("error", foreground="#dc2626")

        bottom = tk.Frame(root, bg="#f3f4f6", padx=14, pady=12)
        bottom.pack(side="bottom", fill="x")

        self.entry = tk.Entry(
            bottom,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
        )
        self.entry.pack(
            side="left", fill="x", expand=True, ipady=10
        )
        self.entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(
            bottom,
            text="Send",
            command=self.send_message,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=9,
        )
        self.send_btn.pack(side="right", padx=(8, 0))

        self.status = tk.StringVar(value="Ready")
        tk.Label(
            root,
            textvariable=self.status,
            bg="#f3f4f6",
            fg="#64748b",
            anchor="w",
        ).pack(side="bottom", fill="x", padx=16)

        self.chat.pack(
            fill="both", expand=True, padx=14, pady=(14, 8)
        )

        self.add_message(
            "Assistant",
            "Hello! Ask me anything. Type a question below.",
            "assistant",
        )
        self.entry.focus_set()

    def add_message(self, sender, message, tag):
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, f"{sender}:\n", tag)
        self.chat.insert(tk.END, f"{message}\n\n")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def send_message(self, event=None):
        prompt = self.entry.get().strip()

        if not prompt:
            return

        self.entry.delete(0, tk.END)
        self.add_message("You", prompt, "user")

        self.send_btn.configure(state="disabled")
        self.status.set("AI is thinking...")

        threading.Thread(
            target=self.get_response,
            args=(prompt,),
            daemon=True,
        ).start()

    def get_response(self, prompt):
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant. Answer the user's questions directly and naturally."
                        "Answer what the user asks, and do not provide additional information unless requested."
                        "Answer in a concise manner. "
                        "Avoid unnecessary formatting."
                        # "use at most 3 short sentences unless the user asks "
                        # "for more detail. Avoid long lists and tables."
                    ),
                },
                *history,
                {"role": "user", "content": prompt},
            ]

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                max_tokens=800,
            )

            answer = (
                response.choices[0].message.content or ""
            )

            history.extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": answer},
            ])

            self.root.after(
                0, self.finish_response, answer, None
            )

        except RateLimitError:
            self.root.after(
                0, self.finish_response, None,
                "Rate limit reached. Please try again later."
            )
        except APIConnectionError:
            self.root.after(
                0, self.finish_response, None,
                "Connection failed. Check your internet."
            )
        except APIStatusError as error:
            self.root.after(
                0, self.finish_response, None,
                f"Groq API error (HTTP {error.status_code})."
            )
        except Exception as error:
            self.root.after(
                0, self.finish_response, None,
                f"Unexpected error: {error}"
            )

    def finish_response(self, answer, error):
        if error:
            self.add_message("Error", error, "error")
            self.status.set("Request failed")
        else:
            self.add_message("Assistant", answer, "assistant")
            self.status.set("Ready")

        self.send_btn.configure(state="normal")
        self.entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = AIChatApp(root)
    root.mainloop()
