
import tkinter as tk
from tkinter import scrolledtext
import threading
import queue

from context_assistant import detect_intent, generate_response


# -----------------------------
# Application state
# -----------------------------

history = []
response_queue = queue.Queue()
is_processing = False


# -----------------------------
# Main window
# -----------------------------

root = tk.Tk()
root.title("Context-Aware AI Assistant")
root.geometry("850x650")
root.minsize(600, 450)
root.configure(bg="#f3f4f6")


# -----------------------------
# Header
# -----------------------------

header = tk.Frame(root, bg="#202938", height=70)
header.pack(fill=tk.X)
header.pack_propagate(False)

title_label = tk.Label(
    header,
    text="AI Chat Assistant",
    font=("Segoe UI", 18, "bold"),
    fg="white",
    bg="#202938",
)
title_label.pack(side=tk.LEFT, padx=20, pady=15)

status_label = tk.Label(
    header,
    text="Ready",
    font=("Segoe UI", 10),
    fg="#a7f3d0",
    bg="#202938",
)
status_label.pack(side=tk.RIGHT, padx=20)


# -----------------------------
# Chat display
# -----------------------------

chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 11),
    bg="white",
    fg="#202938",
    padx=15,
    pady=15,
    spacing1=5,
    spacing3=8,
    state=tk.DISABLED,
    relief=tk.FLAT,
)
chat_area.tag_config(
    "user",
    foreground="#2563eb",
    font=("Segoe UI", 11, "bold"),
)
chat_area.tag_config(
    "assistant",
    foreground="#047857",
    font=("Segoe UI", 11, "bold"),
)
chat_area.tag_config(
    "message",
    foreground="#202938",
    font=("Segoe UI", 11),
)
chat_area.tag_config(
    "system",
    foreground="#6b7280",
    font=("Segoe UI", 9, "italic"),
)


def add_message(sender, message, tag):
    chat_area.configure(state=tk.NORMAL)
    chat_area.insert(tk.END, f"{sender}\n", tag)
    chat_area.insert(tk.END, f"{message}\n\n", "message")
    chat_area.configure(state=tk.DISABLED)
    chat_area.see(tk.END)


# -----------------------------
# Input area
# -----------------------------

input_frame = tk.Frame(root, bg="#f3f4f6")
input_frame.pack(
    side=tk.BOTTOM,
    fill=tk.X,
    padx=15,
    pady=(5, 15),
)

message_entry = tk.Text(
    input_frame,
    height=3,
    wrap=tk.WORD,
    font=("Segoe UI", 11),
    relief=tk.SOLID,
    bd=1,
    padx=10,
    pady=8,
)
message_entry.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True,
    padx=(0, 10),
)


# -----------------------------
# Background API worker
# -----------------------------

def process_message(user_message):
    try:
        intent = detect_intent(user_message, history)

        answer = generate_response(
            message=user_message,
            history=history,
            intent=intent,
        )

        response_queue.put(
            ("success", user_message, intent, answer)
        )

    except Exception as error:
        response_queue.put(
            ("error", user_message, str(error), "")
        )


def send_message(event=None):
    global is_processing

    if is_processing:
        return "break"

    user_message = message_entry.get("1.0", tk.END).strip()

    if not user_message:
        return "break"

    message_entry.delete("1.0", tk.END)

    add_message("You", user_message, "user")

    is_processing = True
    send_button.configure(state=tk.DISABLED)
    status_label.configure(
        text="Thinking...",
        fg="#fcd34d",
    )

    # The API call runs in a worker thread so the window stays responsive.
    worker = threading.Thread(
        target=process_message,
        args=(user_message,),
        daemon=True,
    )
    worker.start()

    return "break"


def check_response_queue():
    global is_processing

    try:
        while True:
            result = response_queue.get_nowait()

            if result[0] == "success":
                _, user_message, intent, answer = result

                # Preserve the conversation for follow-up questions.
                history.extend([
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": answer},
                ])

                add_message(
                    f"Assistant · {intent}",
                    answer,
                    "assistant",
                )

            else:
                _, user_message, error, _ = result

                add_message(
                    "Error",
                    error,
                    "system",
                )

            is_processing = False
            send_button.configure(state=tk.NORMAL)
            status_label.configure(
                text="Ready",
                fg="#a7f3d0",
            )

    except queue.Empty:
        pass

    root.after(100, check_response_queue)


# -----------------------------
# Buttons
# -----------------------------

send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message,
    font=("Segoe UI", 11, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief=tk.FLAT,
    padx=22,
    pady=12,
    cursor="hand2",
)
send_button.pack(side=tk.RIGHT, anchor=tk.S)

# Reserve space for the input controls before expanding the chat display.
chat_area.pack(
    fill=tk.BOTH,
    expand=True,
    padx=15,
    pady=(15, 8),
)

message_entry.bind("<Return>", send_message)

# Shift + Enter inserts a new line.
def insert_newline(event):
    message_entry.insert(tk.INSERT, "\n")
    return "break"


message_entry.bind("<Shift-Return>", insert_newline)


# -----------------------------
# Welcome message and startup
# -----------------------------

add_message(
    "Assistant",
    "Hello! I'm your context-aware AI assistant. "
    "Ask me anything, and I'll use the conversation "
    "to understand your follow-up questions.",
    "assistant",
)

message_entry.focus_set()

root.after(100, check_response_queue)
root.mainloop()
