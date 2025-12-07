#!/bin/bash

# Script to install Gemini SDK

cd "$(dirname "$0")"

echo "📦 Installing Google Generative AI SDK..."
echo ""

# Activate venv
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run ./setup.sh first"
    exit 1
fi

source venv/bin/activate

# Install package
pip install google-generativeai

echo ""
echo "✅ Installation complete!"
echo ""
echo "Make sure you have GEMINI_API_KEY in your .env file:"
echo "  GEMINI_API_KEY=your_gemini_api_key_here"
echo ""
echo "Get your key from: https://aistudio.google.com/app/apikey"

