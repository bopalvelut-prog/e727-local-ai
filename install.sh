#!/bin/bash

# 🤖 Primaclaw: One-Click Installer
# Turns your old hardware into an AI Swarm Node.

set -e

echo "🐚 Primaclaw Installer"
echo "---------------------"

# Check for Python 3.10+
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required."
    exit 1
fi

# Clone if not already in repo
if [ ! -d "src" ]; then
    echo "📦 Cloning Primaclaw..."
    git clone https://github.com/bopalvelut-prog/e727-local-ai.git primaclaw
    cd primaclaw
fi


# Setup Virtual Environment
echo "🐍 Setting up Python Environment..."
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install .

# Setup Default Config
if [ ! -f .env ]; then
    echo "⚙️ Creating default configuration..."
    cp .env.example .env
fi

echo "✅ Installation Complete!"
echo ""
echo "To start the Coordinator (Head Node):"
echo "  source venv/bin/activate && python -m src.coordinator"
echo ""
echo "To start a Worker (Compute Node):"
echo "  source venv/bin/activate && python -m src.worker"
echo ""
echo "🌟 Star us on GitHub: https://github.com/bopalvelut-prog/e727-local-ai"
