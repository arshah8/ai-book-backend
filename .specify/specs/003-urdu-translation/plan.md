# Implementation Plan: Urdu Translation Service

**Branch**: `003-urdu-translation` | **Date**: 2025-01-XX | **Spec**: `.specify/specs/003-urdu-translation/spec.md`  
**Input**: Feature specification for Urdu translation service with caching and OpenAI/Gemini integration.

## Summary

Implement a translation service that converts English textbook content to Urdu using OpenAI/Gemini translation API. The service includes database caching to avoid redundant API calls and preserve formatting.

## Technical Context

- **Language/Version**: Python 3.9+ (FastAPI backend)  
- **Primary Dependencies**: `fastapi`, `app.openai_client` (for translation API), `sqlalchemy`  
- **Storage**: PostgreSQL (Neon) for translation cache  
- **Testing**: Manual testing via `POST /api/translate` endpoint  
- **Target Platform**: Hugging Face Docker Space  
- **Constraints**:
  - Translation API calls are expensive, caching is critical
  - Must preserve code blocks and formatting
  - Cache lookups must be fast (< 100ms)

## Constitution Check

✅ **RAG-First Accuracy**: Translation enables Urdu-speaking users to access textbook content  
✅ **Explicit Configuration**: Translation API key via environment variables  
✅ **Observability**: Translation API failures logged, cache hits/misses tracked  
✅ **Simple Services**: Translation module (`app/translation.py`) provides clear functions  
✅ **Security by Default**: No sensitive data in translation cache

## Project Structure

```text
ai-book-backend/
├── app/
│   ├── translation.py        # Translation functions, cache management
│   ├── openai_client.py      # Translation API integration
│   ├── database.py           # Translation model
│   └── main.py               # POST /api/translate endpoint
└── .specify/specs/
    └── 003-urdu-translation/
        ├── spec.md           # Feature specification
        ├── plan.md           # This file
        └── tasks.md          # Implementation tasks
```

**Structure Decision**: Translation logic is in `app/translation.py` with cache functions. Translation API calls use `app.openai_client.translate_text()`. Cache is stored in PostgreSQL `translations` table.

## Implementation Phases

### Phase 0: Design & Setup ✅ COMPLETE
- Designed translation caching strategy
- Selected database storage for cache (PostgreSQL)
- Planned cache lookup before API call pattern
- Designed Translation model schema

### Phase 1: Database Model ✅ COMPLETE
- Created `Translation` model in `app/database.py`
- Added fields: original_text, translated_text, language, optional module
- Added created_at timestamp for cache management

### Phase 2: Cache Functions ✅ COMPLETE
- Implemented `get_cached_translation()` to lookup existing translations
- Implemented `cache_translation()` to store new translations
- Added error handling for database unavailability

### Phase 3: Translation API Integration ✅ COMPLETE
- Integrated with `app.openai_client.translate_text()` function
- Handled API failures gracefully
- Preserved formatting in translated output

### Phase 4: Translation Endpoint ✅ COMPLETE
- Created `POST /api/translate` endpoint in `app/main.py`
- Implemented cache-first lookup pattern
- Called translation API only if cache miss
- Stored new translations in cache
- Returned translated text

## Complexity Tracking

No constitution violations. Translation service follows simple caching pattern with clear separation between cache and API logic.

