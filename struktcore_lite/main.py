import argparse
import time
import json
import sys

from struktcore_lite.core.plugin_loader import load_plugins
from struktcore_lite.core.prompter import build_prompt
from struktcore_lite.core.model_loader import model
from struktcore_lite.core.memory import append_chat, summarize_chat, write_file, CHAT_LOG, CHAT_SUMMARY, LT_HISTORY, LONG_TERM
from struktcore_lite.core.fuzzy_matcher import match_plugin
from struktcore_lite.core.logger import log
from struktcore_lite.core.config import CONFIG
from struktcore_lite.core.stdin_handler import read_piped_input
from struktcore_lite import __version__ as VERSION

# === Configurable Identity === #
VERSION = CONFIG.get("version", "StruktCore-Lite (dev)")
NAME = CONFIG.get("assistant_name", "SC-L")
SHOW_BANNER = CONFIG.get("shell", {}).get("banner", True)
SHOW_MODEL = CONFIG.get("shell", {}).get("show_model", False)
SHOW_PERSONALITY = CONFIG.get("shell", {}).get("show_personality", False)
MODEL_NAME = CONFIG.get("model", {}).get("model_name", "llama3")
PERSONALITY = CONFIG.get("personality", "No personality defined.")


def print_banner():
    """Displays the CLI startup banner with optional model/personality info."""
    print(f"\n💡 {VERSION}  —  Shell Mode Initialized")
    if SHOW_MODEL:
        print(f"🧠 Model: {MODEL_NAME}")
    if SHOW_PERSONALITY:
        print(f"🧬 Personality: {PERSONALITY}")
    print("Type 'exit' to quit • 'plugins' to list commands • 'help' for help")
    print("-" * 50)


def show_help():
    """Displays available CLI commands."""
    print("\n🆘 Available Commands:")
    print("  help        → Show this message")
    print("  plugins     → List available plugins and aliases")
    print("  exit/quit   → Exit shell mode")
    print("  --plugin    → Force plugin mode for single input")
    print("  --shell     → Enter interactive shell mode")
    print("  --reset     → Wipe memory logs (chat, summary, long-term)")
    print("  --version   → Show current version\n")


def show_plugins():
    """Lists all available plugins with descriptions and aliases."""
    print("\n📦 Available Plugins:\n")
    plugins = load_plugins()
    if not plugins:
        print("No plugins available.\n")
        return

    for name, mod in plugins.items():
        meta = getattr(mod, "metadata", {})
        display_name = meta.get("name", name)
        desc = meta.get("description", "No description.")
        aliases = meta.get("aliases", [])

        print(f"🔹 {display_name}: {desc}")
        if aliases:
            print(f"    ↳ Aliases: {', '.join(aliases)}")
    print()


def run_ai_response(user_input: str) -> str:
    """Processes user input through the AI model and returns a response."""
    log(f"USER: {user_input}", level="IN")
    print(f"[🤖] {NAME} is thinking...\n")
    prompt = build_prompt(user_input)

    try:
        response = model.invoke(prompt).strip()
    except ConnectionError as ce:
        log(f"Ollama not responding: {ce}", level="ERROR")
        print(f"[❌] {NAME} couldn't reach Ollama. Make sure it's running and listening.")
        return ""
    except Exception as e:
        log(f"AI ERROR: {e}", level="ERROR")
        print(f"[❌] {NAME} encountered an unexpected error: {e}")
        return ""

    print(f"[{NAME}]  >> {response}\n")
    print("-" * 60 + "\n")
    append_chat(user_input, response)
    summarize_chat()
    log(f"AI RESPONSE: {response}", level="OUT")
    return response


def run_plugin(input_text: str):
    """Attempts to match and run a plugin from input text."""
    plugins = load_plugins()
    match = match_plugin(input_text, plugins)
    if not match:
        print(f"[❌] No plugin matched: {input_text}")
        log(f"PLUGIN NOT FOUND for input: {input_text}", level="WARN")
        return

    plugin_name, plugin_module = match
    print(f"[⚙️] Running plugin: {plugin_name}")
    log(f"PLUGIN TRIGGERED: {plugin_name}", level="IN")

    start = time.time()
    try:
        plugin_module.run(input_text)
        duration = round(time.time() - start, 2)
        print(f"[✅] Plugin '{plugin_name}' completed in {duration}s")
        log(f"PLUGIN EXECUTED: {plugin_name} in {duration}s", level="OUT")
    except ImportError as ie:
        print(f"[❌] Missing import in plugin '{plugin_name}': {ie}")
        log(f"PLUGIN IMPORT ERROR: {ie}", level="ERROR")
    except Exception as e:
        print(f"[❌] Plugin '{plugin_name}' failed: {e}")
        log(f"PLUGIN ERROR: {plugin_name} -> {e}", level="ERROR")



def reset_memory():
    """Clears memory files (except personality)."""
    for file in [CHAT_LOG, CHAT_SUMMARY, LT_HISTORY, LONG_TERM]:
        write_file(file, "" if file.endswith(".txt") else json.dumps([]))
    log("MEMORY RESET via --reset", level="SYS")
    print("🧠 Memory wiped clean.\n")


def shell_mode():
    """Enters interactive shell mode for continuous conversation."""
    if SHOW_BANNER:
        print_banner()

    while True:
        try:
            user_input = input(f"\n[Strukt] >> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Exiting shell.")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd in {"exit", "quit"}:
            print("👋 Goodbye.")
            break
        elif cmd == "plugins":
            show_plugins()
            continue
        elif cmd == "help":
            show_help()
            continue

        plugins = load_plugins()
        match = match_plugin(user_input, plugins)
        if match:
            run_plugin(user_input)
        else:
            run_ai_response(user_input)


def main():
    """Main CLI entry point for StruktCore-Lite."""
    parser = argparse.ArgumentParser(
    description="StruktCore-Lite: Minimal AI CLI Assistant",
    usage="struktcl 'ask something' [--plugin | --shell | --reset | --list]"
    )       

    parser.add_argument("run", help="Natural language input for plugin or AI", nargs="?")
    parser.add_argument("--plugin", action="store_true", help="Force plugin mode")
    parser.add_argument("--list", action="store_true", help="List available plugins")
    parser.add_argument("--reset", action="store_true", help="Wipe memory (excl. personality)")
    parser.add_argument("--shell", action="store_true", help="Launch interactive shell mode")
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args()

    # === Action Routing === #
    if args.reset:
        reset_memory()
        return
    if args.shell:
        shell_mode()
        return
    if args.list:
        show_plugins()
        return

    # === Handle Input (Piped or Arg) === #
    piped_input = read_piped_input()
    user_query = args.run

    if piped_input and user_query:
        input_text = f"{user_query.strip()}\n\n{piped_input.strip()}"
    elif piped_input:
        default_prompt = CONFIG.get("default_stdin_query", "Explain this:")
        input_text = f"{default_prompt}\n\n{piped_input.strip()}"
    elif user_query:
        input_text = user_query.strip()
    else:
        show_help()
        return

    if args.plugin:
        run_plugin(input_text)
    else:
        run_ai_response(input_text)
