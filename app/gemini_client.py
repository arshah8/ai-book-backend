import os
import time
from pathlib import Path
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from typing import List, Optional

# Load .env file from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Try to import new SDK
try:
    from google import genai
    from google.genai import types
    NEW_SDK_AVAILABLE = True
except ImportError:
    NEW_SDK_AVAILABLE = False
    print("⚠️  New Google GenAI SDK not found. Falling back to legacy SDK.")

import google.generativeai as old_genai
from google.api_core import exceptions as google_exceptions

_gemini_configured = False

def configure_gemini():
    """Configure Gemini API (Legacy SDK), only once"""
    global _gemini_configured
    if not _gemini_configured and GEMINI_API_KEY:
        try:
            old_genai.configure(api_key=GEMINI_API_KEY)
            _gemini_configured = True
        except Exception as e:
            print(f"⚠️  Error configuring Gemini (Legacy): {e}")
    elif not GEMINI_API_KEY:
        print("⚠️  WARNING: GEMINI_API_KEY not set. Chat and translation features may not work.")
        print("   Get your API key from: https://aistudio.google.com/app/apikey")

async def generate_chat_response(
    user_message: str,
    system_context: Optional[str] = None
) -> str:
    """Generate chat response using Gemini (trying Gemini 3 first)"""
    
    if not GEMINI_API_KEY:
        # Try to load again
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
             raise ValueError("GEMINI_API_KEY not configured. Please set it in backend/.env")
    
    # Combine system context and user message
    if system_context:
        full_prompt = f"{system_context}\n\nUser question: {user_message}\n\nAnswer based on the context provided above."
    else:
        full_prompt = user_message

    # 1. Try New SDK with Gemini 3 Pro
    if NEW_SDK_AVAILABLE:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            print(f"Attempting to use gemini-3-pro-preview...")
            
            # Note: thinking_level defaults to "high" for gemini-3-pro-preview.
            response = client.models.generate_content(
                model="gemini-3-pro-preview",
                contents=full_prompt
            )
            print("✅ Using model: gemini-3-pro-preview (New SDK)")
            if response.text:
                return response.text
        except Exception as e:
            print(f"⚠️  Gemini 3 Pro (New SDK) failed: {e}")
            if "429" in str(e):
                 print("   Quota exceeded for Gemini 3 Pro. Falling back to other models.")
            elif "404" in str(e) or "not found" in str(e).lower():
                 print("   Model might not be available for this API key or region.")
            # Fall through to legacy logic

    # 2. Fallback to Legacy SDK
    try:
        configure_gemini()
        
        fallback_models = [
            "gemini-2.5-flash",       # Try 2.5
            "gemini-2.0-flash-lite",  # Newest free tier
            "gemini-2.0-flash",       # Standard 2.0
            "gemini-flash-latest",    # Latest available flash
            "gemini-pro",             # Legacy
        ]
        
        last_error = None
        
        # Iterate through models to find one that works (and has quota)
        for model_name in fallback_models:
            print(f"🔄 Trying fallback model: {model_name}")
            try:
                model = old_genai.GenerativeModel(model_name)
                
                # Generate response with short retry logic per model
                max_retries = 2
                retry_delay = 2
                
                response = None
                for attempt in range(max_retries):
                    try:
                        response = model.generate_content(full_prompt)
                        break
                    except Exception as e:
                        if isinstance(e, google_exceptions.ResourceExhausted):
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay * (attempt + 1))
                                continue
                            else:
                                print(f"   Rate limit on {model_name}, trying next model...")
                                raise e # Re-raise to move to next model in outer loop
                        raise e

                if hasattr(response, 'text') and response.text:
                    print(f"✅ Success with {model_name}")
                    return response.text
                elif hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        text = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                        print(f"✅ Success with {model_name}")
                        return text
                        
            except Exception as e:
                print(f"⚠️  {model_name} failed: {str(e)[:100]}...")
                last_error = e
                continue # Try next model
        
        if last_error:
            # If all models failed, raise the last error (likely a 429 if all are exhausted)
             raise ValueError(f"All Gemini models failed. Last error: {str(last_error)}")
        
        return "I apologize, but I could not generate a response. Please try again."

    except Exception as e:
        print(f"Error generating chat response with Gemini (Legacy): {e}")
        import traceback
        traceback.print_exc()
        raise ValueError(f"Gemini API error: {str(e)}")

async def translate_text(text: str, target_language: str = "ur") -> str:
    """Translate text using Gemini"""
    
    if not GEMINI_API_KEY:
         raise ValueError("GEMINI_API_KEY not configured.")

    language_name = "Urdu" if target_language == "ur" else "English"
    prompt = f"Translate the following text to {language_name}. Preserve formatting, code blocks, and technical terms. Only return the translation:\n\n{text}"

    # 1. Try New SDK
    if NEW_SDK_AVAILABLE:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-3-pro-preview",
                contents=prompt
            )
            if response.text:
                return response.text
        except Exception:
            pass # Fallback silently

    # 2. Fallback to Legacy SDK
    try:
        configure_gemini()
        # Fallback to a fast model available in your list
        model = old_genai.GenerativeModel("gemini-2.0-flash-lite") 
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text') and response.text:
            return response.text
        return text
    except Exception as e:
        print(f"Error translating text: {e}")
        return text
