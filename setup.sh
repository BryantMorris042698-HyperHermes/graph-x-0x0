#!/bin/bash
#
# setup.sh - One-command setup for Graph_x_0x0 AIOS Agent System
# Works on Termux (phone), Linux tablet/laptop, and similar environments.
#
# Usage: ./setup.sh

set -e

echo "=== Graph_x_0x0 Setup for Bryant Issiah Morris Jr. ==="

echo "Creating virtual environment..."
python3 -m venv .venv || { echo "Python 3 venv creation failed. Please ensure python3-venv is installed."; exit 1; }

source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To start the system on any device, run:"
echo "  source .venv/bin/activate"
echo "  python run.py"
echo ""
echo "On Termux (phone), you can also run:"
echo "  bash mobile/termux/termux_bootstrap.sh"
echo ""
echo "See docs/SYSTEM_FRAMEWORK_AND_USER_GUIDE.md for the full framework."