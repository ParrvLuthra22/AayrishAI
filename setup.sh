#!/bin/bash
#
# JARVIS AI Assistant - Setup Script
# Automated installation and configuration
#

echo "🤖 JARVIS AI Assistant Setup"
echo "=============================="

# Check Python version
echo "🔍 Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install optional dependencies for enhanced features
echo "🚀 Installing optional enhancements..."
pip install openai anthropic google-generativeai tavily-python duckduckgo-search

echo ""
echo "✅ JARVIS AI Assistant is now ready!"
echo ""
echo "🚀 To start JARVIS:"
echo "   source .venv/bin/activate"
echo "   python main.py              # GUI mode"
echo "   python main.py --cli        # CLI mode"
echo ""
echo "⚙️  Optional: Add your API keys to .env file:"
echo "   GROQ_API_KEY=your_key_here"
echo "   OPENAI_API_KEY=your_key_here"
echo ""
echo "🎬 'Sometimes you gotta run before you can walk.' - Tony Stark"
