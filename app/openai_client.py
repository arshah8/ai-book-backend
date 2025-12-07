import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Optional
import google.generativeai as genai

# Load .env file from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def configure_gemini():
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)

async def get_embeddings(text: str) -> List[float]:
    """Get embeddings for text using Gemini (text-embedding-004)"""
    try:
        if not GEMINI_API_KEY:
            print("⚠️  GEMINI_API_KEY not set. Embeddings will not work.")
            return create_fallback_embedding(text)
            
        configure_gemini()
        
        # Use Gemini's embedding model
        # "models/text-embedding-004" is the latest standard model
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document",
            title="Embedding of book content"
        )
        
        if 'embedding' in result:
            return result['embedding']
        else:
            print("⚠️  Gemini embedding result empty.")
            return create_fallback_embedding(text)
            
    except Exception as e:
        print(f"Error getting embeddings with Gemini: {e}")
        # Fallback to simple embedding
        return create_fallback_embedding(text)

def create_fallback_embedding(text: str) -> List[float]:
    """Create a simple hash-based embedding as fallback (768 dimensions for Gemini compatibility)"""
    # Note: Gemini embeddings are typically 768 dimensions
    import hashlib
    embedding = [0.0] * 768
    words = text.lower().split()
    
    for i, word in enumerate(words):
        # Create hash from word
        hash_obj = hashlib.md5(word.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        
        # Distribute hash across embedding dimensions
        for j in range(min(10, len(embedding))):
            idx = (hash_int + j) % len(embedding)
            embedding[idx] += 1.0 / (i + 1)
    
    # Normalize
    norm = sum(x * x for x in embedding) ** 0.5
    if norm > 0:
        embedding = [x / norm for x in embedding]
    
    return embedding

async def generate_chat_response(
    user_message: str,
    system_context: Optional[str] = None
) -> str:
    """Generate chat response - now uses Gemini"""
    # Import and use Gemini client instead
    from app.gemini_client import generate_chat_response as gemini_chat
    return await gemini_chat(user_message, system_context)

async def translate_text(text: str, target_language: str = "ur") -> str:
    """Translate text - now uses Gemini"""
    # Import and use Gemini client instead
    from app.gemini_client import translate_text as gemini_translate
    return await gemini_translate(text, target_language)
