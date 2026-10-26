
import os
import re
from pathlib import Path
from string import Template

from dotenv import load_dotenv
from groq import Groq


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. Check your .env file."
    )

client = Groq(api_key=api_key)
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


VALID_INTENTS = {
    "learn_concept",
    "data_analysis",
    "data_cleaning",
    "summarization",
    "planning",
    "general_question",
}


INTENT_INSTRUCTIONS = {
    "learn_concept": (
        "Explain simply in 3-6 sentences. Give one small, "
        "relevant code example when useful. Explain the result briefly."
    ),
    "data_analysis": (
        "Give the key findings and practical insights concisely. "
        "Never invent data."
    ),
    "data_cleaning": (
        "Give the essential steps and a short Python example if useful."
    ),
    "summarization": (
        "Summarize only the main points in a few sentences."
    ),
    "planning": (
        "Give a short, actionable list of the most important steps."
    ),
    "general_question": (
        "Answer directly in 3-6 sentences. Avoid unnecessary details."
    ),
}


conversation_summary = (
    "The user is learning Python, SQL, data analytics, and "
    "LLM application development. Use practical examples "
    "and step-by-step explanations when appropriate."
)


# --------------------------------------------------
# 2. Rule-based intent detection
# --------------------------------------------------

def detect_rule_based_intent(message: str) -> str | None:
    """Recognize common requests without an LLM call."""

    text = message.lower().strip()

    # Data cleaning
    if re.search(
        r"\b(clean|cleaning|deduplicate|duplicates?|"
        r"missing values|impute|null values|"
        r"standardize|normalize)\b",
        text,
    ):
        return "data_cleaning"

    # Data analysis
    if re.search(
        r"\b(analy[sz]e|analysis|analytical|"
        r"trend|correlation|kpi|business insights|"
        r"top-performing|top performing)\b",
        text,
    ):
        return "data_analysis"

    # Summarization
    if re.search(
        r"\b(summarize|summarise|summary|"
        r"give me a summary|key points)\b",
        text,
    ):
        return "summarization"

    # Planning
    if re.search(
        r"\b(create a plan|make a plan|roadmap|"
        r"step-by-step plan|learning plan|"
        r"project plan)\b",
        text,
    ):
        return "planning"

    # Learning and programming questions
    if re.search(
        r"\b(explain|teach me|tutorial|"
        r"what is|what are|how does|how do|"
        r"give me an example|show me an example|"
        r"with an example|example using|"
        r"demonstrate|difference between|"
        r"how to learn)\b",
        text,
    ):
        return "learn_concept"

    return None


# --------------------------------------------------
# 3. LLM-based intent detection
# --------------------------------------------------

def detect_intent(
    message: str,
    history: list[dict] | None = None,
) -> str:

    history = history or []

    # Handle clear requests deterministically first.
    rule_intent = detect_rule_based_intent(message)

    if rule_intent is not None:
        return rule_intent

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intent classifier. Classify the latest "
                "user message into exactly one category:\n"
                "- learn_concept: explanations, learning, tutorials "
                "and programming examples.\n"
                "- data_analysis: analyzing data and finding insights.\n"
                "- data_cleaning: cleaning or validating data.\n"
                "- summarization: summarizing supplied information.\n"
                "- planning: creating plans and roadmaps.\n"
                "- general_question: other questions.\n\n"
                "Use conversation history to interpret follow-ups. "
                "If a follow-up continues a learning discussion, "
                "classify it as learn_concept. "
                "Return only the category identifier."
            ),
        }
    ]

    # Add recent messages in chronological order.
    for item in history[-6:]:
        role = item.get("role")
        content = item.get("content", "")

        if (
            role in {"user", "assistant"}
            and isinstance(content, str)
            and content.strip()
        ):
            messages.append({
                "role": role,
                "content": content[:2000],
            })

    messages.append({
        "role": "user",
        "content": message,
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        max_tokens=50,
    )

    raw_intent = (
        response.choices[0].message.content or ""
    ).strip().lower()

    # Accept a category even if the model adds formatting.
    match = re.search(
        r"\b(" + "|".join(sorted(VALID_INTENTS)) + r")\b",
        raw_intent,
    )

    if match:
        return match.group(1)

    print(f"Warning: Unexpected intent output: {raw_intent!r}")
    return "general_question"


# --------------------------------------------------
# 4. Context-aware response generation
# --------------------------------------------------

def generate_response(
    message: str,
    history: list[dict] | None = None,
    intent: str | None = None,
) -> str:

    history = history or []

    if intent not in VALID_INTENTS:
        intent = detect_intent(message, history)

    context_template = Template("""
You are a helpful, concise AI assistant.

User context:
$summary

Detected intent:
$intent

Instructions:
$instructions

STRICT RESPONSE RULES:
1. Keep answers short, clear, and beginner-friendly.
2. Normally use 3-6 sentences.
3. Give one small code example when necessary.
4. Do not use Markdown formatting.
5. Do not use headings, bold, italics, tables, emojis, or bullet symbols.
6. Do not use Markdown code fences or backticks.
7. When showing code, use plain text and preserve indentation.
8. Answer follow-up questions using relevant conversation history.
9. Explain only what the user asks. Do not repeat previous explanations.
10. Never sacrifice correctness just to keep an answer short.
""")

    system_prompt = context_template.substitute(
        summary=conversation_summary,
        intent=intent,
        instructions=INTENT_INSTRUCTIONS[intent],
    )

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Include recent conversation turns.
    for item in history[-10:]:
        role = item.get("role")
        content = item.get("content", "")

        if (
            role in {"user", "assistant"}
            and isinstance(content, str)
            and content.strip()
        ):
            messages.append({
                "role": role,
                "content": content[:4000],
            })

    # Add the current message exactly once.
    messages.append({
        "role": "user",
        "content": message,
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=800,
    )

    answer = response.choices[0].message.content

    return answer or (
        "I couldn't generate a response. Please try again."
    )


# --------------------------------------------------
# 5. Interactive application
# --------------------------------------------------

def main():
    history = []

    print("Context-Aware AI Assistant (type 'exit' to quit)")

    while True:
        user_message = input("\nYou: ").strip()

        if user_message.lower() == "exit":
            print("Goodbye!")
            break

        if not user_message:
            continue

        try:
            intent = detect_intent(user_message, history)

            print(f"\nDetected intent: {intent}")

            answer = generate_response(
                message=user_message,
                history=history,
                intent=intent,
            )

            print(f"Assistant: {answer}")

            # Save both sides of the successful conversation.
            history.extend([
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": answer},
            ])

        except Exception as error:
            print(f"Request failed: {error}")


if __name__ == "__main__":
    main()
