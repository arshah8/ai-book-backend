# Physical AI Backend Constitution

## Core Principles

### I. RAG-First Accuracy

The backend exists to serve high-quality, textbook-aligned answers.  
- Retrieval pipelines (Qdrant + embeddings) are treated as core infrastructure, not an add-on.  
- When RAG cannot provide context, responses must clearly indicate fallbacks.

### II. Explicit, Reproducible Configuration

All external services (Gemini, Qdrant, Neon DB, auth secrets) are configured via `.env` and documented in `README_ENV.md` / `env.example`.  
- No hard‑coded secrets or cluster URLs.  
- Local, Hugging Face, and future deployments share the same configuration surface.

### III. Observability & Safe Failure

Logging and error handling must make it obvious what went wrong without exposing secrets.  
- Global exception handler returns consistent JSON error envelopes.  
- RAG steps (embeddings, Qdrant search, model fallbacks) log enough detail to debug issues.  
- Fail fast on misconfiguration (e.g., missing QDRANT_URL) with clear messages.

### IV. Simple, Composable Services

The FastAPI app is organized by responsibility (`auth`, `database`, `qdrant_client`, `openai_client`, `translation`, `personalization`).  
- Modules hide implementation details behind clear functions (e.g., `get_qdrant_client`, `search_vectors`, `get_embeddings`).  
- New capabilities should follow the same pattern instead of duplicating logic.

### V. Security by Default

Authentication and authorization are handled centrally.  
- Chat and personalization endpoints accept optional user context, but never trust client input for identity.  
- Tokens and DB URLs are never logged.  
- CORS is permissive for development only and can be tightened for production.

## Backend Constraints & Standards

- **Stack**: Python 3.9+, FastAPI, Qdrant Cloud, PostgreSQL (Neon), Google Gemini API.  
- **Vector Store**: Single `book_content` collection, 768‑dimensional embeddings, cosine distance.  
- **Deployment**: Docker image targeting Hugging Face Spaces (`app_port: 8000`), started via `START_SERVER.sh` or Dockerfile CMD.  
- **Data**: RAG content must be sourced from the canonical Docusaurus markdown (`ai-book-frontend/book/docs`) using the `scripts/seed_vectors.py` pipeline.

## Workflow & Quality Gates

- Changes that affect RAG or auth must be reflected in:  
  - `specs/` (feature spec, plan, tasks)  
  - `README.md` / `RATE_LIMIT_GUIDE.md` / related docs where relevant.  
- Before deploying, run `TEST_ENV.py` / `VERIFY_ENV.sh` and a quick manual `/api/chat` sanity check against seeded content.  
- Any breaking change to the embedding model, collection name, or payload structure requires an updated spec and a clear migration path.

## Governance

This constitution guides how the backend evolves:  
- New features and refactors SHOULD reference and comply with these principles.  
- Amendments MUST be documented in `specs/` and linked from relevant ADRs or README files.  
- When trade‑offs are made (e.g., reduced logging, different models), they must be justified in the corresponding spec or ADR.

**Version**: 1.0.0 | **Ratified**: 2025-01-XX | **Last Amended**: 2025-01-XX
