from rapidfuzz import process
from rapidfuzz import fuzz
from struktcore_lite.core.config import CONFIG

def match_plugin(user_input, plugins):
    alias_map = {}

    for name, module in plugins.items():
        meta = getattr(module, "metadata", {})
        aliases = meta.get("aliases", [])
        display_name = meta.get("name", name)  # fallback to filename if no name

        # Ensure we always include the filename and optional name
        search_terms = aliases + [name, display_name]

        for alias in search_terms:
            alias_map[alias] = name

    if not alias_map:
        return None

    threshold = CONFIG.get("plugins", {}).get("fuzzy_threshold", 60)
    best_match, score, _ = process.extractOne(user_input, alias_map.keys())
    
    if score < threshold:
        return None

    matched_plugin = alias_map[best_match]
    return matched_plugin, plugins[matched_plugin]
