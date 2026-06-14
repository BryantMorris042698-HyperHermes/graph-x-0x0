#!/data/data/com.termux/files/usr/bin/bash
#
# termux_bootstrap.sh
# One-command bootstrap for Graph_x_0x0 on Galaxy Z Fold7 (Termux)
# Personalized exclusively for Bryant Issiah Morris Jr.
# Sets up venv, installs dependencies, configures truth mode, and launches the mobile dashboard/REPL.
# Run with: bash mobile/termux/termux_bootstrap.sh

set -e

echo "=== Graph_x_0x0 Mobile Bootstrap for Bryant Issiah Morris Jr. ==="
echo "This system is authorized exclusively for Bryant Issiah Morris Jr."
echo "Truth mode: Responses grounded in deterministic Φ(G) computation or MemePlace retrieval only."

# Check Termux environment
if [ ! -d "/data/data/com.termux/files/usr" ]; then
    echo "Error: This script must be run inside Termux."
    exit 1
fi

# Update packages (minimal)
pkg update -y && pkg install -y python git clang make libffi openssl 2>/dev/null || true

# Create dedicated venv
VENV_DIR="$HOME/graphx0x0-mobile-venv"
if [ ! -d "$VENV_DIR" ]; then
    python -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

echo "Virtual environment activated: $VENV_DIR"

# Install Python dependencies (lightweight for phone)
pip install --upgrade pip
pip install rich prompt_toolkit  # rich for dashboard visuals; prompt_toolkit for better REPL

# Ensure repo is present (assume user cloned to ~/graph-x-0x0 or current dir has it)
REPO_DIR="$(pwd)"
if [ ! -f "$REPO_DIR/python/high_agent_engine/graph.py" ]; then
    echo "Please run this script from the root of the graph-x-0x0 repository (or cd into it first)."
    exit 1
fi

# Add repo to PYTHONPATH
export PYTHONPATH="$REPO_DIR:$PYTHONPATH"

# Optional: Start local SLM server reminder
echo ""
echo "IMPORTANT: Ensure your local SLM/LLM server is running (llama.cpp recommended)."
echo "Example: ./llama-server -m /path/to/your-quantized-model.gguf --port 8080"
echo "Set SLM_ENDPOINT=http://localhost:8080/v1 in environment if different."
echo ""

# Launch the personalized mobile dashboard
echo "Launching personalized TUI for Bryant Issiah Morris Jr...."
python "$REPO_DIR/mobile/termux/mobile_dashboard.py"
