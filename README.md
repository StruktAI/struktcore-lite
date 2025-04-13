# 🧠 StruktCore-Lite
---

![428220337-fd2d33e4-1b0c-4fa0-b705-22c06eabbecb](https://github.com/user-attachments/assets/3863a3cd-4b8d-4dd7-bac8-b442d72904e8)

---

Minimal. Terminal-native. Extendable.  
**StruktCore-Lite** is a plugin-based AI assistant built for CLI environments — designed for developers who want *control*, not clutter.

---

### ⚡ Features

- ✅ Ollama LLM integration (LLaMA3 by default)  
- 🧩 Dynamic plugin system with fuzzy matching  
- 📁 Memory system: logs, summaries, long-term retention  
- 🧠 Configurable AI personality via `assets/sc-l.yaml`  
- ⌨️ **Supports piped input** from stdin (e.g. `cat file | struktcl`)  
- 💡 Easy YAML-based config  
- 🔐 Fully local — no external API calls  
- 🧪 Simple testing via `pytest`  
- 🧱 Clean modular structure for extending core functionality  

---

### 📦 Installation

```bash
git clone https://github.com/StruktAI/struktcore-lite.git
cd struktcore-lite
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install .
```

✅ This installs a CLI tool called `struktcl`.

ℹ️ On first run, `struktcl` will create local `memory/` and `logs/` folders  
to store logs, summaries, personality, and system activity.

---

### 🚀 Usage

#### 🔁 Launch shell mode:
```bash
struktcl --shell
```

#### 💬 Run a direct AI command:
```bash
struktcl "What's the capital of France?"
```

#### 🧩 Force plugin mode:
```bash
struktcl "restart nginx" --plugin
```

#### 📥 Pipe into the assistant:
```bash
cat file.txt | struktcl "Summarise this:"
```

Or use default prompt:
```bash
echo "Some code" | struktcl
```

#### ♻️ Reset memory:
```bash
struktcl --reset
```

---

### ⚙️ Configuration

Edit the YAML file at: `assets/sc-l.yaml`

Example:

```yaml
version: "StruktCore-Lite v0.1.2"
assistant_name: "SC-L"
personality: "Minimal, efficient, terminal-native AI assistant."

model:
  model_name: "llama3"
  temperature: 0.7

plugins:
  fuzzy_threshold: 75

shell:
  banner: true
  show_model: true
  show_personality: true
```

---

### 🧩 Plugins

Plugins are matched using:

- `aliases` from `metadata`
- the plugin filename
- `metadata["name"]` (if provided)

Each plugin lives in the `plugins/` folder and must define a `run()` function.

Example:

```python
# plugins/example_plugin.py

metadata = {
    "name": "Restart NGINX",
    "description": "Restarts the NGINX service.",
    "aliases": ["restart nginx", "reload web server"]
}

def run(input_text=None):
    print("Restarting nginx...")
```

---

### 🧠 Memory

AI memory logs are stored in the `memory/` directory:

- `chat_log.json` — raw conversation history  
- `chat_summary.txt` — running summary  
- `long_term_memory.txt` — retained memory  
- `lt_summary_history.txt` — archived summaries

Reset memory:
```bash
struktcl --reset
```

---

### 🛠️ Development

While editing the assistant core:

```bash
struktcl --shell
```

Work inside:

```
struktcore_lite/core/
```

---

### 🧪 Testing

Run tests with:

```bash
pytest tests/
```

---

### 📄 License

MIT — see [`LICENSE`](LICENSE)

---

### 🚧 Roadmap Ideas

- [ ] Plugin scheduling / crontab support  
- [ ] Dynamic LLM switching  
- [ ] REST API interface  
- [ ] Plugin discovery via Git sync  

---

### 👤 Built by Gus

> “Structure is survival.”  
> If you like this project, fork it, star it, or drop in your own modules.
