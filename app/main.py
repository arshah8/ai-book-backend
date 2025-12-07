from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from backend directory BEFORE importing other modules
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from app.database import get_db, init_db
from app.qdrant_client import get_qdrant_client, search_vectors
from app.openai_client import get_embeddings, generate_chat_response
from app.models import ChatRequest, ChatResponse, TranslateRequest, TranslateResponse
from app.auth import get_current_user_optional, router as auth_router

app = FastAPI(title="Physical AI Textbook API", version="1.0.0")

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    """Initialize database and Qdrant on startup"""
    try:
        await init_db()
    except Exception as e:
        print(f"⚠️  Database initialization skipped: {e}")
        print("   Some features may not work without database connection")
    
    try:
        await get_qdrant_client()
    except Exception as e:
        print(f"⚠️  Qdrant initialization skipped: {e}")
        print("   Vector search may not work without Qdrant connection")

@app.get("/")
async def root():
    return {"message": "Physical AI Textbook API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """RAG chatbot endpoint"""
    try:
        # Get embeddings for query (with fallback)
        context_text = ""
        try:
            query_embedding = await get_embeddings(request.message or request.context)
            
            if query_embedding and len(query_embedding) > 0:
                # Search Qdrant for relevant chunks
                try:
                    qdrant_client = await get_qdrant_client()
                    search_results = await search_vectors(qdrant_client, query_embedding, limit=5)
                    # Build context from search results
                    context_text = "\n\n".join([result["text"] for result in search_results])
                except Exception as e:
                    print(f"⚠️  Qdrant search failed: {e}")
                    print("   Using fallback context")
            else:
                print("⚠️  No embeddings available, using fallback context")
        except Exception as e:
            print(f"⚠️  Embedding generation failed: {e}")
            print("   Using fallback context")
        
        # Fallback context if no vector search results
        if not context_text:
            context_text = "This is a textbook about Physical AI & Humanoid Robotics covering ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action systems."
        
        # Add selected text context if provided
        if request.context:
            context_text = f"{request.context}\n\n{context_text}"
        
        # Generate response using OpenAI
        system_prompt = f"""You are an AI assistant helping students learn about Physical AI & Humanoid Robotics. 
Use the following context from the textbook to answer questions accurately. If the context doesn't contain 
the answer, you can use your general knowledge but indicate when you're doing so.

Context from textbook:
{context_text}

Answer the question based on the context provided. Be helpful, clear, and educational."""
        
        # Generate response using Gemini
        try:
            response = await generate_chat_response(
                user_message=request.message or request.context,
                system_context=system_prompt
            )
        except Exception as e:
            print(f"Error generating chat response: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to generate response. Please check GEMINI_API_KEY is set correctly. Error: {str(e)}"
            )
        
        # Store chat history if user is logged in
        if current_user and current_user.get("id"):
            try:
                from app.database import save_chat_history
                await save_chat_history(
                    user_id=current_user["id"],
                    message=request.message or request.context,
                    response=response,
                    context=request.context
                )
            except Exception as e:
                print(f"Warning: Could not save chat history: {e}")
                # Continue even if history save fails
        
        return ChatResponse(response=response)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"Unexpected error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """Translate content to Urdu"""
    try:
        from app.translation import translate_text, get_cached_translation
        
        # Check cache first
        cached = await get_cached_translation(request.text, request.language)
        if cached:
            return TranslateResponse(translated_text=cached)
        
        # Translate using OpenAI
        translated = await translate_text(request.text, request.language)
        
        # Cache the translation
        from app.translation import cache_translation
        await cache_translation(request.text, translated, request.language, request.module)
        
        return TranslateResponse(translated_text=translated)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/personalize")
async def get_personalization(
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Get personalization settings for current user"""
    try:
        if not current_user or not current_user.get("id"):
            from app.personalization import get_default_config
            return get_default_config()
        
        from app.personalization import get_user_personalization
        config = await get_user_personalization(current_user["id"])
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

