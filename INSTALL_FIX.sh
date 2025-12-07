#!/bin/bash

# Quick fix script for installation issues

echo "🔧 Fixing Backend Installation"
echo ""

cd "$(dirname "$0")"

# Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Activated virtual environment"
else
    echo "❌ Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip3 install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"

