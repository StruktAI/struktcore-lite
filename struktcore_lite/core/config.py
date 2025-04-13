import yaml
import os

# === Define default config path relative to package ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "assets", "sc-l.yaml")

# === Load config YAML ===
def load_config(path=CONFIG_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing config file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

CONFIG = load_config()
