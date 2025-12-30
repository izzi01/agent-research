#!/bin/bash
# Quick Start Script for Vietnamese Marketing Automation
# Using UV - The blazing-fast Python package manager

set -e  # Exit on error

echo "🚀 Vietnamese Marketing Automation - Quick Start"
echo "================================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version || { echo "❌ Python 3.8+ required"; exit 1; }

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "📦 UV not found. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "✓ UV version: $(uv --version)"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment with UV..."
    uv venv .venv
    echo "✓ Virtual environment created!"
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/bin/activate

# Install dependencies with UV
echo "📦 Installing dependencies with UV..."
echo "   This will take ~10-30 seconds!"
uv pip install -r requirements.txt
echo "✓ Dependencies installed!"

echo ""
echo "========================================================"
echo "🎯 READY TO START!"
echo "========================================================"
echo ""
echo "Choose an option:"
echo ""
echo "1. TEST WITH MOCK DATA (no API keys needed)"
echo "   Run: python test_textcreator.py"
echo ""
echo "2. START API SERVER (needs GLM API key)"
echo "   a. Edit .env and add your ZHIPU_API_KEY"
echo "   b. Start PostgreSQL: docker run -d --name postgres-pgvector -e POSTGRES_USER=agno -e POSTGRES_PASSWORD=changeme123 -e POSTGRES_DB=marketing_automation -p 5432:5432 pgvector/pgvector:pg16"
echo "   c. Run: python main.py"
echo ""
echo "========================================================"
echo ""

# Ask user what to do
read -p "Run test script now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🧪 Running test script with mock data..."
    echo ""
    python test_textcreator.py
fi
