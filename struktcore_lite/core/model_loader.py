# struktcore_lite/core/model_loader.py
from struktcore_lite.core.config import CONFIG
from langchain_ollama import OllamaLLM

MODEL_CONFIG = CONFIG.get("model", {})
MODEL_NAME = MODEL_CONFIG.get("model_name", "llama3")
TEMPERATURE = MODEL_CONFIG.get("temperature", 0.7)

model = OllamaLLM(model=MODEL_NAME, temperature=TEMPERATURE)
