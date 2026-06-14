"""run.py

Unified AIOS Agent Chat + TUI Launcher
Optimized for phone (Termux), tablet, and laptop.
Auto-detects device and selects best interface.

Exclusive to Bryant Issiah Morris Jr.
Truth mode enforced at all times.

Usage:
  python run.py                 # Auto-detect + launch best interface
  python run.py --chat          # Force chat mode
  python run.py --dashboard     # Force dashboard mode
  python run.py --aios          # Launch with AIOS kernel integration

This is the single entry point for your entire agentic system.
"""

import os
import sys
import platform
import argparse

# Ensure we can import local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rich.console import Console
    from rich.panel import Panel
except ImportError:
    print("rich is required. Please run: pip install rich")
    sys.exit(1)

console = Console()


def detect_device():
    """Auto-detect device type."""
    if 'com.termux' in os.environ.get('PREFIX', '') or os.path.exists('/data/data/com.termux'):
        return 'phone'
    elif 'ANDROID' in os.environ.get('TERM', '') or 'Android' in platform.platform():
        return 'tablet'  # Could be refined with screen size
    else:
        # Check for common laptop/desktop indicators
        if os.name == 'posix' and 'linux' in platform.system().lower():
            return 'laptop'
        return 'desktop'


def verify_identity():
    name = input("Confirm your identity (full name): ").strip().lower()
    if name != "bryant issiah morris jr":
        print("Access denied. This system is for Bryant Issiah Morris Jr. only.")
        sys.exit(1)
    print("Identity verified: Bryant Issiah Morris Jr.")
    return True


def get_truth_prefix():
    return (
        "You are operating exclusively for Bryant Issiah Morris Jr. "
        "Respond ONLY with information that is either (1) direct mathematical result from Graph_x_0x0 "
        "or (2) accurately retrieved/summarized from MemePlace. "
        "If unverifiable, say 'Insufficient verified information'. Truth only. No speculation."
    )


def launch_chat():
    from mobile.termux.mobile_chat import run_chat
    run_chat()

def launch_dashboard():
    from mobile.termux.mobile_dashboard import run_mobile_dashboard
    run_mobile_dashboard()

def launch_aios_mode():
    console.print(Panel("AIOS Kernel integration mode selected.", title="AIOS"))
    console.print("For full AIOS experience, see integration/aios/README.md")
    console.print("You can still use chat or dashboard while AIOS kernel runs on another device.")
    # Future: connect to remote or local AIOS kernel
    launch_chat()  # Fallback for now


def main():
    parser = argparse.ArgumentParser(description="Graph_x_0x0 AIOS Agent Launcher for Bryant Issiah Morris Jr.")
    parser.add_argument('--chat', action='store_true', help='Force chat mode')
    parser.add_argument('--dashboard', action='store_true', help='Force dashboard mode')
    parser.add_argument('--aios', action='store_true', help='Launch with AIOS integration')
    args = parser.parse_args()

    device = detect_device()
    console.print(Panel(f"Device detected: [bold]{device}[/bold] | User: Bryant Issiah Morris Jr. | Truth Mode", border_style="blue"))

    if not verify_identity():
        return

    if args.chat:
        launch_chat()
    elif args.dashboard:
        launch_dashboard()
    elif args.aios:
        launch_aios_mode()
    else:
        # Smart default based on device
        if device == 'phone':
            console.print("Phone detected → Launching lightweight Chat interface...")
            launch_chat()
        elif device in ('tablet', 'laptop', 'desktop'):
            console.print("Tablet/Laptop detected → Launching full Dashboard...")
            launch_dashboard()
        else:
            launch_chat()

if __name__ == "__main__":
    main()
