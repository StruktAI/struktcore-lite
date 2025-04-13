import os
from datetime import datetime
from struktcore_lite.core.config import CONFIG

# === Configurable Log Directory & File === #
LOG_DIR = CONFIG.get("logging", {}).get("directory", "logs")
LOG_FILE = os.path.join(LOG_DIR, CONFIG.get("logging", {}).get("log_file", "system.log"))
LOG_ENABLED = CONFIG.get("logging", {}).get("enabled", True)

os.makedirs(LOG_DIR, exist_ok=True)

def log(message, level="INFO"):
    if not LOG_ENABLED:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [{level.upper()}] {message}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")
