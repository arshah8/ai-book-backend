import os
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from typing import List, Dict, Optional

# Load .env file from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

COLLECTION_NAME = "book_content"
QDRANT_URL = os.getenv("QDRANT_URL", "https://your-cluster.qdrant.io")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")

# Clean up QDRANT_URL - fix common typos
if QDRANT_URL:
    QDRANT_URL = QDRANT_URL.strip()
    # Fix double 'h' typo: hhttps -> https
    if QDRANT_URL.startswith("hhttps"):
        QDRANT_URL = "https" + QDRANT_URL[6:]
    # Fix http/https typos
    if QDRANT_URL.startswith("http://") and "qdrant" in QDRANT_URL:
        QDRANT_URL = QDRANT_URL.replace("http://", "https://", 1)
    # Remove quotes
    QDRANT_URL = QDRANT_URL.strip("'\"")

_qdrant_client: Optional[QdrantClient] = None

async def get_qdrant_client() -> QdrantClient:
    """Get or create Qdrant client"""
    global _qdrant_client
    if _qdrant_client is None:
        # Validate URL before creating client
        if not QDRANT_URL or QDRANT_URL == "https://your-cluster.qdrant.io":
            raise ValueError("QDRANT_URL not configured")
        
        try:
            _qdrant_client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY if QDRANT_API_KEY else None,
            )
            await ensure_collection()
        except Exception as e:
            print(f"Error creating Qdrant client: {e}")
            raise
    return _qdrant_client

async def ensure_collection():
    """Ensure Qdrant collection exists"""
    try:
        collections = _qdrant_client.get_collections()
        collection_exists = any(c.name == COLLECTION_NAME for c in collections.collections)
        
        if not collection_exists:
            _qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=768,  # Gemini text-embedding-004 dimension
                    distance=Distance.COSINE
                )
            )
            print(f"Created Qdrant collection: {COLLECTION_NAME}")
    except Exception as e:
        print(f"Error ensuring collection: {e}")

async def search_vectors(
    client: QdrantClient,
    query_vector: List[float],
    limit: int = 5
) -> List[Dict]:
    """Search for similar vectors in Qdrant"""
    try:
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )
        
        return [
            {
                "text": result.payload.get("text", ""),
                "score": result.score,
                "id": str(result.id),
                "module": result.payload.get("module"),
                "section": result.payload.get("section")
            }
            for result in results
        ]
    except Exception as e:
        print(f"Error searching vectors: {e}")
        return []

async def add_vector(
    client: QdrantClient,
    vector_id: str,
    vector: List[float],
    payload: Dict
):
    """Add vector to Qdrant collection"""
    try:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                {
                    "id": vector_id,
                    "vector": vector,
                    "payload": payload
                }
            ]
        )
    except Exception as e:
        print(f"Error adding vector: {e}")
        raise

