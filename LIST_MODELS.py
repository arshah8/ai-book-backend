#!/usr/bin/env python3
"""
Script to list available Gemini models
Run: python3 LIST_MODELS.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not set in .env file")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

print("🔍 Listing available Gemini models...")
print("")

try:
    models = genai.list_models()
    
    print("Available models that support generateContent:")
    print("-" * 60)
    
    available = []
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            available.append(model.name)
            print(f"✅ {model.name}")
            if hasattr(model, 'display_name'):
                print(f"   Display Name: {model.display_name}")
            print()
    
    if available:
        print(f"\n✅ Found {len(available)} model(s)")
        print(f"\nRecommended free tier model: {available[0] if available else 'None'}")
    else:
        print("❌ No models found that support generateContent")
        
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\nTrying common model names manually...")
    
    common_models = ['gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.5-flash-latest']
    for model_name in common_models:
        try:
            model = genai.GenerativeModel(model_name)
            print(f"✅ {model_name} - Available")
        except Exception as e:
            print(f"❌ {model_name} - Not available: {str(e)[:80]}")

