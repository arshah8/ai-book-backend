# Feature Specification: Urdu Translation Service

**Feature Branch**: `003-urdu-translation`  
**Created**: 2025-01-XX  
**Status**: ✅ Complete  
**Input**: User description: "Urdu translation service with caching and OpenAI integration"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Translate Content to Urdu (Priority: P1)

A user can request translation of textbook content from English to Urdu. The system translates the content using OpenAI/Gemini API and returns the translated text while preserving formatting and code blocks.

**Why this priority**: Urdu translation makes the textbook accessible to Urdu-speaking learners, significantly expanding the user base and educational impact.

**Independent Test**: Can be fully tested by calling `POST /api/translate` with English text and verifying:
- Translated Urdu text is returned
- Translation is accurate and preserves meaning
- Response time is acceptable (< 5 seconds for typical content)

**Acceptance Scenarios**:

1. **Given** a user requests translation of English text, **When** they call `/api/translate` with text and language="ur", **Then** the system returns translated Urdu text.
2. **Given** the same text is translated again, **When** the user requests translation, **Then** the system returns cached translation immediately without calling the translation API.
3. **Given** a translation request includes code blocks or special formatting, **When** the text is translated, **Then** code blocks and formatting are preserved in the translated output.

---

### User Story 2 - Translation Caching for Performance (Priority: P2)

The system caches translations in the database to avoid redundant API calls. When the same text is requested again, the cached translation is returned immediately.

**Why this priority**: Translation API calls are expensive and slow. Caching reduces costs and improves response times for frequently accessed content.

**Independent Test**: Can be fully tested by:
- Requesting translation for a text
- Requesting the same translation again
- Verifying second request uses cache (faster response, no API call)

**Acceptance Scenarios**:

1. **Given** a text has been translated before, **When** the same text is requested for translation, **Then** the cached translation is returned from database.
2. **Given** a text has not been translated before, **When** translation is requested, **Then** the system calls translation API, stores result in cache, and returns translation.

---

### Edge Cases

- What happens when translation API fails? → System returns 500 error with clear message, translation is not cached.
- How does system handle very long text (> 4000 tokens)? → Text is chunked or truncated, or error is returned if too long.
- What if database is unavailable for caching? → Translation still works but caching is skipped, warning is logged.
- How are special characters and Unicode handled? → System preserves Unicode encoding, Urdu characters are correctly stored and returned.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide `POST /api/translate` endpoint that accepts text and language parameters.
- **FR-002**: System MUST translate English text to Urdu using OpenAI/Gemini translation API.
- **FR-003**: System MUST cache translations in database with original_text, translated_text, language, and optional module fields.
- **FR-004**: System MUST check cache before calling translation API and return cached result if available.
- **FR-005**: System MUST preserve code blocks, formatting, and special characters in translated output.
- **FR-006**: System MUST handle translation API failures gracefully with appropriate error responses.
- **FR-007**: System MUST support module-specific caching to enable per-module translation management.

### Key Entities *(include if feature involves data)*

- **Translation**: Represents a cached translation with id, original_text, translated_text, language (e.g., "ur"), optional module, and created_at timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Translation API responds within 5 seconds for typical textbook content (1-2 paragraphs).
- **SC-002**: Cached translations are returned within 100ms (database lookup time).
- **SC-003**: Translation accuracy is verified by manual review of sample translations (target: 95%+ accuracy).
- **SC-004**: Cache hit rate is > 80% for repeated translation requests of the same content.
- **SC-005**: System handles translation API failures without crashing, returns appropriate error messages.
