# Implementation Plan: Backend RAG Sync with Physical AI Textbook

**Branch**: `001-rag-sync-book-content` | **Date**: 2025-01-XX | **Spec**: `specs/001-rag-sync-book-content/spec.md`  
**Input**: Feature specification describing markdown → embeddings → Qdrant pipeline.

## Summary

Update the backend RAG so that it reads the latest Docusaurus markdown from the frontend repo, chunks it into semantically coherent pieces, embeds each chunk with Gemini, and stores them in a single Qdrant collection (`book_content`).  
The `/api/chat` endpoint then uses these vectors to assemble context for Gemini chat responses.

## Technical Context

- **Language/Version**: Python 3.9.x (FastAPI backend)  
- **Primary Dependencies**: `fastapi`, `qdrant-client`, `google-generativeai` / `google-genai`, `sqlalchemy`, `python-dotenv`  
- **Storage**: Qdrant Cloud (`book_content` collection), Neon PostgreSQL for auth/history  
- **Testing**: `TEST_ENV.py`, `TEST_CHAT.py` and manual `/api/chat` runs via frontend  
- **Target Platform**: Hugging Face Docker Space (`uvicorn app.main:app` on port 8000)  
- **Constraints**:
  - Embedding dimension fixed at 768 to match collection config.  
  - Qdrant URL/API key and GEMINI_API_KEY come from env only.  
  - Seeder must tolerate partial failures and log them clearly.

## Project Structure (this feature)

```text
ai-book-backend/
├── app/
│   ├── main.py           # /api/chat RAG endpoint (uses search_vectors + Gemini)
│   ├── qdrant_client.py  # get_qdrant_client, ensure_collection, search_vectors, add_vector
│   └── openai_client.py  # get_embeddings(), generate_chat_response() using Gemini
├── scripts/
│   └── seed_vectors.py   # NEW: reads frontend markdown, chunks, embeds, upserts to Qdrant
└── specs/
    └── 001-rag-sync-book-content/
        ├── spec.md       # RAG feature specification
        └── plan.md       # This file
```

**Structure Decision**: Single backend project with a dedicated `scripts/` folder for operational tooling (seeding, env checks). RAG remains part of the main FastAPI app, not a separate service.

## High-level Phases (retroactive)

1. **Phase 0 – Design RAG update (DONE)**  
   - Decide to use the Docusaurus markdown in `ai-book-frontend/book/docs` as the single source of truth.  
   - Keep Qdrant collection name and vector size stable (`book_content`, 768).

2. **Phase 1 – Implement seeding pipeline (DONE)**  
   - Implement `scripts/seed_vectors.py`:
     - Discover markdown files under `book/docs`.  
     - Strip front-matter and chunk by paragraphs.  
     - Infer `module` and `section` metadata from file paths.  
     - Optionally reset the collection before inserting.  
   - Use `get_embeddings` and `add_vector` for each chunk.

3. **Phase 2 – Integrate with `/api/chat` (DONE)**  
   - Keep using `search_vectors()` in `app.main.chat`.  
   - Confirm logs show that Qdrant is queried and that retrieved payloads contain `text/module/section`.  
   - Ensure fallback context still works when no vectors are available.

4. **Phase 3 – Verification & iteration (IN PROGRESS)**  
   - Run seeding locally and on Hugging Face.  
   - Ask targeted questions about each module and capstone to verify retrieved context.  
   - Tune chunk size or module/section inference if any gaps are found.

## Complexity Tracking

No constitution violations identified so far; RAG functionality builds on existing Qdrant + Gemini stack using straightforward scripts and helpers.


