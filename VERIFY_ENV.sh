#!/bin/bash

# Script to verify .env file is being loaded

cd "$(dirname "$0")"

echo "🔍 Verifying .env file configuration"
echo ""

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Run test script
python3 TEST_ENV.py

