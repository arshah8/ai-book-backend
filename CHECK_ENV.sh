#!/bin/bash

# Script to check if environment variables are set

echo "🔍 Checking Backend Environment Variables"
echo ""

cd "$(dirname "$0")"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Creating .env from example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✓ Created .env file"
        echo ""
        echo "⚠️  Please edit .env and add your API keys:"
        echo "   - OPENAI_API_KEY"
        echo "   - QDRANT_URL and QDRANT_API_KEY"
        echo "   - DATABASE_URL"
        echo "   - BETTER_AUTH_SECRET"
    else
        echo "❌ env.example not found!"
        exit 1
    fi
else
    echo "✓ .env file exists"
fi

echo ""
echo "Checking required variables:"
echo ""

# Load .env file
if [ -f ".env" ]; then
    source .env
fi

# Check each variable
MISSING=0

if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "❌ OPENAI_API_KEY not set"
    MISSING=1
else
    echo "✓ OPENAI_API_KEY is set"
fi

if [ -z "$QDRANT_URL" ] || [ "$QDRANT_URL" = "https://your-cluster-id.qdrant.io" ]; then
    echo "❌ QDRANT_URL not set"
    MISSING=1
else
    echo "✓ QDRANT_URL is set"
fi

if [ -z "$DATABASE_URL" ] || [ "$DATABASE_URL" = "postgresql://user:password@host.neon.tech/dbname?sslmode=require" ]; then
    echo "❌ DATABASE_URL not set"
    MISSING=1
else
    echo "✓ DATABASE_URL is set"
fi

if [ -z "$BETTER_AUTH_SECRET" ] || [ "$BETTER_AUTH_SECRET" = "your_random_secret_key_min_32_characters_long" ]; then
    echo "❌ BETTER_AUTH_SECRET not set"
    MISSING=1
else
    echo "✓ BETTER_AUTH_SECRET is set"
fi

echo ""

if [ $MISSING -eq 1 ]; then
    echo "⚠️  Some environment variables are missing or not configured"
    echo "   Please edit backend/.env and add your API keys"
    echo "   See ENV_SETUP.md for instructions"
    exit 1
else
    echo "✅ All environment variables are configured!"
fi

