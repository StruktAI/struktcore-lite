# 🧠 StruktCore-Lite

Minimal. Terminal-native. Extendable.  
**StruktCore-Lite** is a plugin-based AI assistant built for CLI environments — designed for developers who want *control*, not clutter.

---

### ⚡ Features

- ✅ Ollama LLM integration (LLaMA3 by default)  
- 🧩 Dynamic plugin system with fuzzy matching  
- 📁 Memory logging: chat history, summaries, long-term  
- 🧠 AI persona loaded from `memory/personality.txt` (configured via `assets/sc-l.yaml`)  
- 💡 Simple YAML config in `assets/sc-l.yaml`  
- 🔐 Local-first, runs entirely on your machine  

---

### 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/struktcore-lite.git
cd struktcore-lite
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install .
```

> ✅ This installs a CLI tool called `StruktCL`.

> ℹ️ On first run, `StruktCL` will create local `memory/` and `logs/` folders in your working directory
> to store conversation logs, summaries, personality, and system activity.

---

### 🚀 Usage

#### Launch interactive shell:

```bash
StruktCL --shell
```

#### Run a command directly:

```bash
StruktCL "What's the capital of France?"
```

#### Force plugin mode:

```bash
StruktCL "run disk-check" --plugin
```

---

### ⚙️ Config

Edit the YAML file at:
```
assets/sc-l.yaml
```

Example:
```yaml
version: "StruktCore-Lite v0.1.2"
assistant_name: "SC-L"
personality: "Minimal, efficient, terminal-native AI assistant."

model:
  model_name: "llama3"
  temperature: 0.7

shell:
  banner: true
  show_model: true
  show_personality: true
```

---

### 🧩 Plugins

> 🧩 Plugins are matched using:
> - `aliases` from metadata (recommended)
> - the plugin filename (e.g. `example_plugin`)
> - `metadata['name']` if defined


All plugins live in the `plugins/` folder and must define a `run()` method and optional metadata:

```python
# plugins/example_plugin.py

metadata = {
    "description": "Says hello.",
    "aliases": ["hello", "greet"]
}

def run(input_text=None):
    print("Hello from plugin!")
```

---

### 🧠 Memory

Memory logs are stored in the `memory/` folder:

- `chat_log.json` — raw history  
- `chat_summary.txt` — running summary  
- `long_term_memory.txt` — condensed memory  
- `lt_summary_history.txt` — archive of summaries  

Reset memory via:

```bash
StruktCL --reset
```

---

### 🛠️ Dev Mode

To hack on the assistant:

```bash
StruktCL --shell
```

While modifying files inside:
```
struktcore_lite/core/
```

---

### 🧪 Testing (optional)

If you've added tests:

```bash
pytest tests/
```

---

### 📄 License

MIT — see [`LICENSE`](LICENSE) file.

---

### 🚧 Roadmap Ideas

- [ ] Plugin scheduling / crontab support  
- [ ] Dynamic LLM switching  
- [ ] REST API wrapper  
- [ ] Plugin marketplace via Git sync  

---

### 🤖 Built with 💀 by Gus

> “Structure is survival.”  
> If you like this project, fork it, drop a star, or plug in your own assistant modules.
