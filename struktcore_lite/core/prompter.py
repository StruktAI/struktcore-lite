import os, datetime
from struktcore_lite.core.memory import read_file, load_json
from struktcore_lite.core.config import CONFIG

# === Memory Paths === #
MEMORY_CONFIG = CONFIG.get("memory", {})

CHAT_LOG = MEMORY_CONFIG.get("chat_log", "memory/chat_log.json")
CHAT_SUMMARY = MEMORY_CONFIG.get("summary", "memory/chat_summary.txt")
LONG_TERM = MEMORY_CONFIG.get("long_term", "memory/long_term_memory.txt")
LT_HISTORY = MEMORY_CONFIG.get("lt_history", "memory/lt_summary_history.txt")
PERSONALITY = MEMORY_CONFIG.get("personality_file", "memory/personality.txt")

# === Prompt Builder === #
def build_prompt(user_input):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    personality = CONFIG.get("personality", "Minimal, efficient, terminal-native AI assistant.")
    summary = read_file(CHAT_SUMMARY)
    long_term = read_file(LONG_TERM)
    chat = load_json(CHAT_LOG)[-6:]

    def fmt(x):
        if x.get("role") == "user":
            return f"User: {x['text']}"
        elif x.get("role") == "ai":
            return f"AI: {x['text']}"
        return ""

    recent = "\n".join([fmt(x) for x in chat if fmt(x)])

    base_prompt = CONFIG.get("prompt_template", """
Respond as SC-L — a minimal, insightful AI CLI assistant.

Your replies should:
- Be direct and focused
- Never repeat what the user already said unless needed
- Avoid small talk unless explicitly prompted
- Use clean, structured language
- Never say “glad we’re talking” or “happy to help”
- Avoid excessive friendliness or filler

Behave more like a conversational interface in a terminal, not a chatbot.

Only use paragraph breaks when shifting ideas or clarifying.

Your personality is:
{personality}

The current time is {now}.

Here's your long-term memory:
{long_term}

Recent summary:
{summary}

Recent chat:
{recent}

User: {user_input}
AI:
""")

    prompt = base_prompt.format(
        personality=personality,
        now=now,
        long_term=long_term or "No long-term memory yet.",
        summary=summary or "No summary available yet.",
        recent=recent or "No recent conversation found.",
        user_input=user_input
    )

    return prompt.strip()
