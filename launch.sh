#!/bin/bash
#
# JARVIS AI Assistant - Launch Script
# Quick launcher with environment activation
#

echo "🤖 Launching JARVIS AI Assistant..."
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

source .venv/bin/activate

if [ "$1" = "--cli" ] || [ "$1" = "-c" ]; then
    echo "🖥️ Starting JARVIS in CLI mode..."
    python main.py --cli
else
    echo "🖼️ Starting JARVIS in GUI mode..."
    python main.py
fi
