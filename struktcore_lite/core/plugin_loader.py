import importlib.util
import os
from typing import Dict
from types import ModuleType
from struktcore_lite.core.config import CONFIG
from struktcore_lite.core.logger import log

PLUGIN_DIR = CONFIG.get("plugins", {}).get("path", "plugins")

def load_plugins() -> Dict[str, ModuleType]:
    """Loads plugins from the configured directory."""
    plugins = {}
    abs_path = os.path.abspath(PLUGIN_DIR)

    if not os.path.exists(abs_path):
        log(f"PLUGIN DIRECTORY NOT FOUND: {abs_path}", level="WARN")
        return plugins

    for file in os.listdir(abs_path):
        if file.endswith(".py") and not file.startswith("__"):
            name = file[:-3]
            path = os.path.join(abs_path, file)

            try:
                spec = importlib.util.spec_from_file_location(name, path)
                if not spec or not spec.loader:
                    log(f"FAILED TO LOAD SPEC FOR: {file}", level="ERROR")
                    continue

                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                if hasattr(mod, "run"):
                    plugins[name] = mod
                else:
                    log(f"PLUGIN SKIPPED (no run()): {name}", level="DEBUG")
            except Exception as e:
                log(f"PLUGIN LOAD ERROR ({name}): {e}", level="ERROR")
    
    return plugins