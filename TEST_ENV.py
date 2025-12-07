#!/usr/bin/env python3
"""
Quick test script to verify .env file is being loaded correctly
Run: python3 TEST_ENV.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / '.env'
print(f"Loading .env from: {env_path}")
print(f"File exists: {env_path.exists()}")

if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    print("✓ .env file loaded")
else:
    print("❌ .env file not found!")
    exit(1)

print("\nChecking environment variables:")
print("-" * 50)

vars_to_check = [
    "OPENAI_API_KEY",
    "QDRANT_URL",
    "QDRANT_API_KEY",
    "DATABASE_URL",
    "BETTER_AUTH_SECRET"
]

all_set = True
for var in vars_to_check:
    value = os.getenv(var)
    if value and value not in ["your_openai_api_key_here", "https://your-cluster-id.qdrant.io", 
                               "postgresql://user:password@host.neon.tech/dbname?sslmode=require",
                               "your_random_secret_key_min_32_characters_long"]:
        # Show first and last few characters for security
        masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
        print(f"✓ {var}: {masked}")
    else:
        print(f"❌ {var}: NOT SET or using placeholder")
        all_set = False

print("-" * 50)
if all_set:
    print("\n✅ All environment variables are properly configured!")
else:
    print("\n⚠️  Some environment variables need to be set in .env file")

