"""run.py

Unified AIOS Agent Chat + TUI Launcher
Optimized for phone (Termux), tablet, and laptop.
Auto-detects device and selects best interface.

Exclusive to Bryant Issiah Morris Jr.
Truth mode enforced at all times.

This script now includes basic first-run checks.
"""

import os
import sys
import platform
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rich.console import Console
    from rich.panel import Panel
except ImportError:
    print("rich not installed. Please run ./setup.sh first.")
    sys.exit(1)

console = Console()


def detect_device():
    if 'com.termux' in os.environ.get('PREFIX', '') or os.path.exists('/data/data/com.termux'):
        return 'phone'
    elif 'ANDROID' in os.environ.get('TERM', '') or 'Android' in platform.platform():
        return 'tablet'
    else:
        return 'laptop'


def verify_identity():
    name = input("Confirm your identity (full name): ").strip().lower()
    if name != "bryant issiah morris jr":
        print("Access denied. This system is for Bryant Issiah Morris Jr. only.")
        sys.exit(1)
    print("Identity verified: Bryant Issiah Morris Jr.")
    return True

def get_truth_prefix():
    return "You are operating exclusively for Bryant Issiah Morris Jr. Respond ONLY with verifiable Graph_x_0x0 results or MemePlace content. Truth only."

def launch_chat():
    from mobile.termux.mobile_chat import run_chat
    run_chat()

def launch_dashboard():
    from mobile.termux.mobile_dashboard import run_mobile_dashboard
    run_mobile_dashboard()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chat', action='store_true')
    parser.add_argument('--dashboard', action='store_true')
    parser.add_argument('--aios', action='store_true')
    args = parser.parse_args()

    device = detect_device()
    console.print(Panel(f"Device detected: {device} | Bryant Issiah Morris Jr. | Truth Mode", border_style="blue"))

    if not verify_identity():
        return

    if args.chat:
        launch_chat()
    elif args.dashboard:
        launch_dashboard()
    elif args.aios:
        from integration.aios.graph_x_tool import GraphXTool
        print("AIOS mode - using GraphXTool directly.")
        tool = GraphXTool()
        print(tool.theory_explain())
    else:
        if device == 'phone':
            launch_chat()
        else:
            launch_dashboard()

if __name__ == "__main__":
    main()
