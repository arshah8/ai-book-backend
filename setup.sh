#!/bin/bash

# Backend setup script for macOS/Linux
# This script helps set up the Python virtual environment

set -e

echo "🔧 Setting up Backend Environment"
echo ""

# Check for Python 3
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
    echo "✓ Found python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
    echo "✓ Found python"
else
    echo "❌ Python not found!"
    echo ""
    echo "Please install Python 3.10+ from:"
    echo "  - https://www.python.org/downloads/"
    echo "  - Or using Homebrew: brew install python3"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "  Python version: $PYTHON_VERSION"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
$PIP_CMD install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "To start the backend server:"
echo "  uvicorn app.main:app --reload"

