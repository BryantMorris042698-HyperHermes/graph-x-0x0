"""run.py

Unified launcher with smart LLM backend detection.
Now supports Ollama out of the box (just do ollama pull <model>).
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rich.console import Console
    from rich.panel import Panel
except ImportError:
    print("Please run ./setup.sh first")
    sys.exit(1)

console = Console()

def main():
    from llm_client import get_llm_endpoint, is_llm_available

    print("Detecting LLM backend...")
    endpoint = get_llm_endpoint()
    available = is_llm_available()

    if available:
        console.print(Panel(f"LLM backend ready: {endpoint}", border_style="green"))
    else:
        console.print(Panel("No LLM detected. Running in pure deterministic mode (still fully functional).", border_style="yellow"))

    # ... rest of device detection and launch logic ...
    from mobile.termux.mobile_chat import run_chat
    from mobile.termux.mobile_dashboard import run_mobile_dashboard

    device = 'phone' if 'com.termux' in os.environ.get('PREFIX', '') else 'laptop'
    if device == 'phone':
        run_chat()
    else:
        run_mobile_dashboard()

if __name__ == "__main__":
    main()
