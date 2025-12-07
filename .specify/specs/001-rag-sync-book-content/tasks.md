# Tasks: Backend RAG Sync with Physical AI Textbook

**Input**: `spec.md` and `plan.md` under `specs/001-rag-sync-book-content/`  
**Prerequisites**: Backend FastAPI app and Qdrant client already in place.

## Phase 1: Setup & Plumbing (DONE)

- [x] T001 [P] [US1] Add script entry point `scripts/seed_vectors.py` that can be run via `python -m scripts.seed_vectors`.  
- [x] T002 [P] [US1] Ensure backend can locate `ai-book-frontend/book/docs` via a relative path from the backend root.  
- [x] T003 [P] [US1] Import `get_qdrant_client`, `add_vector`, and `get_embeddings` for reuse in the seeding script.

## Phase 2: Chunking & Metadata (DONE)

- [x] T010 [US1] Implement `chunk_text(text, max_chars)` to split markdown into paragraph-based chunks (~1400 chars).  
- [x] T011 [US1] Implement `infer_module_and_section(md_path)` to map markdown paths to `module` and `section`.  
- [x] T012 [US1] Implement `load_book_chunks()` to walk `book/docs`, strip front-matter, and build a list of `{text, module, section}`.

## Phase 3: Qdrant Integration (DONE)

- [x] T020 [P] [US1] Extend `qdrant_client.py` to expose `COLLECTION_NAME` and `ensure_collection()`.  
- [x] T021 [US1] In `seed_vectors.py`, optionally reset `book_content` (delete + recreate) before inserting new points.  
- [x] T022 [US1] For each chunk, generate an embedding via `get_embeddings(text)` and upsert into Qdrant with payload `{text,module,section}`.  
- [x] T023 [US1] Log per-chunk progress and final totals to make seeding observable.

## Phase 4: Chat Endpoint & RAG Verification (PARTIAL)

- [x] T030 [US1] Confirm `/api/chat` continues to call `search_vectors()` and uses `payload["text"]` to build `context_text`.  
- [x] T031 [US1] Add logging in `app.main.chat` to show whether RAG is active, how many chunks were retrieved, and top scores.  
- [ ] T032 [US1] Add a small internal test script or notebook that issues representative questions and prints retrieved module/section metadata for manual QA.

## Phase 5: Documentation & Operationalization (PARTIAL)

- [x] T040 [US2] Document the seeding workflow in `README.md` / `DEPLOY_HUGGINGFACE.md` (at least basic command + env requirements).  
- [x] T041 [US2] Add `specs/001-rag-sync-book-content/spec.md` and `plan.md` describing the RAG pipeline.  
- [ ] T042 [US2] Add a short “RAG maintenance” section to `DASHBOARD_GUIDE.md` or a new ops doc explaining when to reseed and how to validate.  
- [ ] T043 [US2] Consider a lightweight health/diagnostic endpoint or CLI command that verifies Qdrant connectivity and collection schema.

## Phase 6: Nice-to-haves (FUTURE)

- [ ] T050 [US2] Support partial reseeding for a single module or section (e.g., `--module module2`).  
- [ ] T051 [US2] Track basic RAG usage metrics (e.g., how often Qdrant returns 0 results) for future tuning.


