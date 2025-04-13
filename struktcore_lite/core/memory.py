import os, json, datetime
from langchain_ollama import OllamaLLM
from struktcore_lite.core.config import CONFIG
from struktcore_lite.core.model_loader import model

# === File Paths ===
MEMORY_DIR = "memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

MEMORY_CONFIG = CONFIG.get("memory", {})

CHAT_LOG = MEMORY_CONFIG.get("chat_log", "memory/chat_log.json")
CHAT_SUMMARY = MEMORY_CONFIG.get("summary", "memory/chat_summary.txt")
LONG_TERM = MEMORY_CONFIG.get("long_term", "memory/long_term_memory.txt")
LT_HISTORY = MEMORY_CONFIG.get("lt_history", "memory/lt_summary_history.txt")
PERSONALITY = MEMORY_CONFIG.get("personality_file", "memory/personality.txt")

# === Model (for summarization) ===
MODEL_CONFIG = CONFIG.get("model", {})
MODEL_NAME = MODEL_CONFIG.get("model_name", "llama3")
TEMPERATURE = MODEL_CONFIG.get("temperature", 0.7)
model = OllamaLLM(model=MODEL_NAME, temperature=TEMPERATURE)

# === File Helpers ===
def read_file(path):
    return open(path).read().strip() if os.path.exists(path) else ""

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except json.JSONDecodeError:
        return []

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

# === Personality ===
def load_personality():
    if not os.path.exists(PERSONALITY):
        write_file(PERSONALITY, "Supportive, strategic, emotionally aware, efficient, proactive.")
    return read_file(PERSONALITY)

# === Append Chat ===
def append_chat(user_text, ai_response):
    chat = load_json(CHAT_LOG)
    timestamp = datetime.datetime.now().isoformat()
    chat.append({"role": "user", "text": user_text, "timestamp": timestamp})
    chat.append({"role": "ai", "text": ai_response, "timestamp": timestamp})
    save_json(CHAT_LOG, chat)

# === Summarize Chat if Needed ===
def summarize_chat():
    chat = load_json(CHAT_LOG)
    if len(chat) < 8 or len(chat) % 6 != 0:
        return
    recent = chat[-20:]
    lines = []
    for i in range(0, len(recent), 2):
        if i + 1 < len(recent):
            user = recent[i]
            ai = recent[i + 1]
            if user["role"] == "user" and ai["role"] == "ai":
                lines.append(f"User: {user['text']}\nAI: {ai['text']}")
    flat = "\n".join(lines)
    if not flat:
        return
    summary = model.invoke(f"Summarize this conversation:\n\n{flat}").strip()
    write_file(CHAT_SUMMARY, summary)
    history = read_file(LT_HISTORY)
    full = "\n---\n".join(filter(None, [history, summary]))
    write_file(LT_HISTORY, full)
    update_long_term()

# === Condense to Long-Term Memory ===
def update_long_term():
    history = read_file(LT_HISTORY).split("\n---\n")
    if len(history) >= 5:
        recent = "\n".join(history[-5:])
        condensed = model.invoke(f"Condense the following conversation summaries into long-term memory:\n\n{recent}").strip()
        write_file(LONG_TERM, condensed)
        write_file(LT_HISTORY, "\n---\n".join(history[:-5]))
