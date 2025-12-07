#!/bin/bash

# Script to start the backend server with proper environment setup

echo "🚀 Starting Backend Server"
echo ""

cd "$(dirname "$0")"

# Check environment
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "   Creating from example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✓ Created .env file"
        echo ""
        echo "❌ Please edit .env and add your API keys before starting the server"
        echo "   See ENV_SETUP.md for instructions"
        exit 1
    fi
fi

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run ./setup.sh first"
    exit 1
fi

source venv/bin/activate

# Check if uvicorn is installed
if ! command -v uvicorn &> /dev/null; then
    echo "⚠️  uvicorn not found. Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "Starting server..."
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

