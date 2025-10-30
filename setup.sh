#!/bin/bash

# Setup script for DSPy Tree-of-Thought Demo

echo "🚀 Setting up DSPy Tree-of-Thought Demo"
echo "======================================"
echo

# Check if .env exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo
    echo "⚠️  IMPORTANT: Please edit .env and add your OpenRouter API key:"
    echo "   OPENROUTER_API_KEY=your-actual-openrouter-api-key-here"
    echo
else
    echo "✅ .env file already exists"
fi

# Check for required packages
echo "📦 Checking for required packages..."

if ! python3 -c "import dspy" 2>/dev/null; then
    echo "❌ DSPy not found. Installing..."
    pip install dspy-ai
    echo "✅ DSPy installed"
else
    echo "✅ DSPy is installed"
fi

echo
echo "🎯 Setup complete!"
echo
echo "Next steps:"
echo "1. Edit .env and add your OPENROUTER_API_KEY"
echo "2. Run: python run_demo.py"
echo
echo "Happy coding! 🎉"