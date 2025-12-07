"""
Script to seed Qdrant with book content embeddings.

This version reads the latest markdown from the Docusaurus book
and chunks it automatically, so RAG always stays in sync with
your textbook content.

Usage (from project root or backend folder):

    python -m scripts.seed_vectors

Make sure QDRANT_URL, QDRANT_API_KEY and GEMINI_API_KEY are set.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict
import uuid

# Add backend directory to path so "app" imports work
BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(BACKEND_ROOT))

from app.qdrant_client import (  # type: ignore
    get_qdrant_client,
    add_vector,
    COLLECTION_NAME,
    ensure_collection,
)
from app.openai_client import get_embeddings  # type: ignore

# Path to the Docusaurus markdown docs in the frontend project
FRONTEND_ROOT = BACKEND_ROOT.parent / "ai-book-frontend"
DOCS_ROOT = FRONTEND_ROOT / "book" / "docs"

# Control whether we wipe and recreate the collection before seeding
RESET_COLLECTION = True


def chunk_text(text: str, max_chars: int = 1400) -> List[str]:
  """
  Simple paragraph-based chunker.
  Keeps paragraphs together up to max_chars to preserve structure.
  """
  paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
  chunks: List[str] = []
  current: List[str] = []
  current_len = 0

  for p in paragraphs:
      if current_len + len(p) + 2 <= max_chars:
          current.append(p)
          current_len += len(p) + 2
      else:
          if current:
              chunks.append("\n\n".join(current))
          current = [p]
          current_len = len(p)

  if current:
      chunks.append("\n\n".join(current))

  return chunks


def infer_module_and_section(md_path: Path) -> Dict[str, str]:
  """
  Infer module and section labels from file path.
  Examples:
    docs/intro.md                -> module='intro',   section='intro'
    docs/module1/introduction.md -> module='module1', section='introduction'
    docs/capstone/overview.md    -> module='capstone', section='overview'
  """
  rel = md_path.relative_to(DOCS_ROOT)
  parts = rel.parts

  if len(parts) == 1:
      # e.g. intro.md
      module = "intro"
      section = md_path.stem
  else:
      module = parts[0]
      section = md_path.stem

  return {"module": module, "section": section}


def load_book_chunks() -> List[Dict[str, str]]:
  """
  Walk the docs directory and build a list of text chunks with metadata.
  """
  if not DOCS_ROOT.exists():
      raise RuntimeError(f"Docs root not found at {DOCS_ROOT}. Make sure the frontend repo is present.")

  chunks: List[Dict[str, str]] = []

  for md_path in sorted(DOCS_ROOT.rglob("*.md")):
      raw = md_path.read_text(encoding="utf-8")

      # Strip simple front-matter if present
      if raw.startswith("---"):
          parts = raw.split("---", 2)
          if len(parts) == 3:
              raw = parts[2]

      raw = raw.strip()
      if not raw:
          continue

      meta = infer_module_and_section(md_path)
      text_chunks = chunk_text(raw)

      for chunk_text_value in text_chunks:
          chunks.append(
              {
                  "text": chunk_text_value,
                  "module": meta["module"],
                  "section": meta["section"],
              }
          )

  return chunks


async def seed_vectors():
  """Seed Qdrant with book content from markdown docs."""
  print(f"📚 Loading markdown from: {DOCS_ROOT}")
  book_chunks = load_book_chunks()
  print(f"Starting vector seeding...")
  print(f"Total chunks to process: {len(book_chunks)}")
  
  qdrant_client = await get_qdrant_client()
  
  if RESET_COLLECTION:
      print(f"🧹 Resetting Qdrant collection '{COLLECTION_NAME}'...")
      try:
          qdrant_client.delete_collection(COLLECTION_NAME)
      except Exception as e:
          print(f"  (Skipping delete, may not exist yet): {e}")
      await ensure_collection()

  for i, chunk in enumerate(book_chunks, 1):
      print(f"[{i}/{len(book_chunks)}] {chunk['module']}/{chunk['section']}...")
      
      # Get embedding
      embedding = await get_embeddings(chunk["text"])
      if not embedding:
          print("  ⚠️  Failed to get embedding")
          continue
      
      vector_id = str(uuid.uuid4())
      await add_vector(
          qdrant_client,
          vector_id,
          embedding,
          {
              "text": chunk["text"],
              "module": chunk["module"],
              "section": chunk["section"],
          },
      )
      
      print(f"  ✓ Added vector ({len(embedding)} dimensions)")
  
  print(f"\n✅ Vector seeding complete! Added {len(book_chunks)} chunks to Qdrant")


if __name__ == "__main__":
    asyncio.run(seed_vectors())

