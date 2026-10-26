
from flask import Flask, request, jsonify
from context_assistant import detect_intent, generate_response
import uuid

app = Flask(__name__)

# Demo storage. Conversations reset when the server restarts.
conversations = {}


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()
    conversation_id = data.get("conversation_id", "")

    if not isinstance(message, str) or not message:
        return jsonify({"error": "Please enter a message."}), 400

    if len(message) > 10000:
        return jsonify({"error": "Message is too long."}), 400

    if not isinstance(conversation_id, str):
        return jsonify({"error": "Invalid conversation ID."}), 400

    if not conversation_id:
        conversation_id = str(uuid.uuid4())

    history = conversations.setdefault(conversation_id, [])

    try:
        intent = detect_intent(message, history)

        answer = generate_response(
            message=message,
            history=history,
            intent=intent,
        )

        history.extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": answer},
        ])

        return jsonify({
            "conversation_id": conversation_id,
            "intent": intent,
            "answer": answer,
        })

    except Exception:
        app.logger.exception("Chat request failed")
        return jsonify({
            "error": "The AI request failed. Please try again."
        }), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
