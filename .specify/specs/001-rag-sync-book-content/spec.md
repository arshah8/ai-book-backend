# Feature Specification: Backend RAG Sync with Physical AI Textbook

**Feature Branch**: `001-rag-sync-book-content`  
**Created**: 2025-01-XX  
**Status**: ✅ Complete  
**Input**: "Update the backend RAG so it reads the new Docusaurus book content, chunks it properly, and keeps Qdrant in sync with the textbook used by the frontend."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Chatbot answers from the latest book content (Priority: P1)

A learner asks questions in the frontend chatbot and receives answers based on the *current* Physical AI & Humanoid Robotics textbook stored in the `book/docs` directory.

**Why this priority**: Without fresh embeddings, the assistant can drift away from the actual course material.

**Independent Test**:

- Run the seeding script and verify it processes all markdown files in `ai-book-frontend/book/docs`.
- Ask questions about specific sections (e.g., Gazebo Simulation, URDF, VLA) and confirm answers reference content that exists in those markdown files.

**Acceptance Scenarios**:

1. **Given** the book markdown has been updated, **When** `python -m scripts.seed_vectors` is run, **Then** Qdrant’s `book_content` collection is recreated and populated with embeddings derived from the new files.  
2. **Given** Qdrant is healthy and seeded, **When** `/api/chat` is called with a question about a seeded topic, **Then** logs show a successful Qdrant search and the response uses the retrieved context.

---

### User Story 2 - RAG seeding is reproducible and automatic (Priority: P2)

Developers can re-seed the RAG at any time with a single command, without manually editing scripts when the book structure changes.

**Why this priority**: The book will evolve; the backend must track those changes with low friction.

**Independent Test**:

- Add a new markdown file under `book/docs/moduleX/`.
- Re-run the seeding script.
- Confirm the new section appears in the logs and can be queried via the chatbot.

**Acceptance Scenarios**:

1. **Given** a new markdown file is added under `book/docs`, **When** the seeder runs, **Then** the logs show at least one `[.../section-name...]` entry for that file.  
2. **Given** the seeder is run twice, **When** inspecting Qdrant, **Then** the collection is reset and repopulated cleanly without duplicate points or schema errors.

---

### Edge Cases

- What happens when the frontend repo is missing or the `book/docs` path is incorrect? → Seeder should fail fast with a clear error message.  
- How does the system behave if Qdrant credentials are wrong? → Seeder should report connection failures and avoid partial, inconsistent writes.  
- What if Gemini embeddings fail for some chunks? → Script should log failures and continue with the rest, rather than aborting silently.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The backend MUST load markdown content recursively from `../ai-book-frontend/book/docs`.  
- **FR-002**: The seeding script MUST chunk markdown into reasonably sized pieces (e.g., ~1.4k characters) while keeping paragraph boundaries where possible.  
- **FR-003**: Each chunk added to Qdrant MUST include payload fields: `text`, `module`, and `section` inferred from the file path.  
- **FR-004**: The script MUST support resetting the `book_content` collection before inserting new vectors (to avoid stale data).  
- **FR-005**: The `/api/chat` endpoint MUST continue to use `search_vectors` from `qdrant_client` and pass the resulting `text` into the Gemini prompt context.  
- **FR-006**: Seeding MUST use the same embedding model (dimension 768) as configured in the Qdrant collection.

### Key Entities

- **Book Chunk**: A slice of markdown text with associated `module` and `section`, used as a single Qdrant point.  
- **Embedding Vector**: 768‑dimensional float list representing a chunk, produced by `get_embeddings`.  
- **Qdrant Point**: `{ id, vector, payload }` stored in the `book_content` collection.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `python -m scripts.seed_vectors` completes without uncaught exceptions and reports all processed chunks in the console.  
- **SC-002**: Qdrant’s `book_content` collection contains at least one point for every markdown file present in `book/docs`.  
- **SC-003**: For at least 90% of sampled questions tied to specific sections (URDF, Gazebo, Isaac, VLA, Capstone), the assistant uses RAG context (confirmed via backend logs showing non-empty `search_results`).  
- **SC-004**: Re-running the seeder after editing markdown results in updated answers that reflect the new content (no stale text from removed sections).


