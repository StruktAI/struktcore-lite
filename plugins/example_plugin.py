# plugins/example_plugin.py
import os

metadata = {
    "name": "Restart NGINX",
    "description": "Restarts the NGINX service on your system.",
    "aliases": ["restart nginx", "reload web server", "fix nginx"]
}

def run(input_text=None):
    print("Restarting nginx...")
    os.system("sudo systemctl restart nginx")