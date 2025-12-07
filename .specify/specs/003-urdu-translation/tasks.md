# Tasks: Urdu Translation Service

**Input**: `spec.md` and `plan.md` under `.specify/specs/003-urdu-translation/`  
**Prerequisites**: Database infrastructure (005-database-infrastructure) must be in place.

## Phase 1: Database Model (DONE)

- [x] T001 [P] Create `Translation` model in `app/database.py`
- [x] T002 [P] Add fields: original_text, translated_text, language, optional module
- [x] T003 [P] Add created_at timestamp field
- [x] T004 [P] Ensure `translations` table is created in `init_db()`

## Phase 2: Cache Functions (DONE)

- [x] T010 [US2] Implement `get_cached_translation(original_text, language)` in `app/translation.py`
- [x] T011 [US2] Query database for existing translation matching original_text and language
- [x] T012 [US2] Return cached translation if found, None otherwise
- [x] T013 [US2] Implement `cache_translation(original_text, translated_text, language, module)` in `app/translation.py`
- [x] T014 [US2] Store new translation in database
- [x] T015 [US2] Handle database errors gracefully (return None, log warning)

## Phase 3: Translation API Integration (DONE)

- [x] T020 [US1] Integrate with `app.openai_client.translate_text()` function
- [x] T021 [US1] Pass text and target language to translation API
- [x] T022 [US1] Handle API failures with appropriate error messages
- [x] T023 [US1] Preserve formatting and code blocks in translated output

## Phase 4: Translation Endpoint (DONE)

- [x] T030 [US1] Create `TranslateRequest` model with text and language fields
- [x] T031 [US1] Create `TranslateResponse` model with translated_text field
- [x] T032 [US1] Create `POST /api/translate` endpoint in `app/main.py`
- [x] T033 [US1] Check cache first using `get_cached_translation()`
- [x] T034 [US1] Return cached translation if available
- [x] T035 [US1] Call translation API if cache miss
- [x] T036 [US1] Store new translation in cache using `cache_translation()`
- [x] T037 [US1] Return translated text in response
- [x] T038 [US1] Handle translation API failures (500 error with clear message)

## Phase 5: Testing & Verification (DONE)

- [x] T040 [US1] Test translation of English text to Urdu
- [x] T041 [US2] Test cache hit (same text translated twice, second call uses cache)
- [x] T042 [US1] Test cache miss (new text, API call is made)
- [x] T043 [US1] Test error handling when translation API fails
- [x] T044 [US1] Test error handling when database is unavailable (cache skipped)

## Completed Features Summary

✅ **Translation API**: English to Urdu translation using OpenAI/Gemini  
✅ **Caching**: Database cache prevents redundant API calls  
✅ **Performance**: Cache lookups < 100ms, API calls only on cache miss  
✅ **Error Handling**: Graceful degradation when API or database unavailable  
✅ **Format Preservation**: Code blocks and formatting preserved in translations

**All user stories (US1, US2) are complete and independently testable.**

