# Tasks: Content Personalization Service

**Input**: `spec.md` and `plan.md` under `.specify/specs/004-content-personalization/`  
**Prerequisites**: Database infrastructure (005-database-infrastructure) and authentication (002-user-authentication) must be in place.

## Phase 1: Config Functions (DONE)

- [x] T001 [US1] Implement `get_default_config()` in `app/personalization.py`
- [x] T002 [US1] Return default config: show_advanced_topics=true, show_code_examples=true, code_complexity="standard", explanation_depth="detailed"
- [x] T003 [US1] Implement `get_config_for_level(experience_level)` function
- [x] T004 [US1] Create BEGINNER config: show_advanced_topics=false, code_complexity="simple", explanation_depth="detailed"
- [x] T005 [US1] Create INTERMEDIATE config: show_advanced_topics=true, code_complexity="standard", explanation_depth="detailed"
- [x] T006 [US1] Create ADVANCED config: show_advanced_topics=true, code_complexity="advanced", explanation_depth="comprehensive"

## Phase 2: User Personalization (DONE)

- [x] T010 [US1] Implement `get_user_personalization(user_id)` in `app/personalization.py`
- [x] T011 [US1] Query UserProfile from database using user_id
- [x] T012 [US1] Extract experience_level from user profile
- [x] T013 [US1] Call `get_config_for_level()` with user's experience_level
- [x] T014 [US1] Return config for user's level
- [x] T015 [US1] Handle missing user profile (return default config)
- [x] T016 [US1] Handle invalid experience_level (default to BEGINNER)

## Phase 3: Personalization Endpoint (DONE)

- [x] T020 [US1] Create `GET /api/personalize` endpoint in `app/main.py`
- [x] T021 [US1] Use `get_current_user_optional` dependency for optional authentication
- [x] T022 [US1] If user is authenticated, call `get_user_personalization(user_id)`
- [x] T023 [US1] If user is not authenticated, return default config
- [x] T024 [US1] Return config as JSON response
- [x] T025 [US1] Handle database errors gracefully (return default config)

## Phase 4: Testing & Verification (DONE)

- [x] T030 [US1] Test endpoint with authenticated beginner user (returns beginner config)
- [x] T031 [US1] Test endpoint with authenticated intermediate user (returns intermediate config)
- [x] T032 [US1] Test endpoint with authenticated advanced user (returns advanced config)
- [x] T033 [US1] Test endpoint with unauthenticated user (returns default config)
- [x] T034 [US1] Test endpoint with user missing profile (returns default config)
- [x] T035 [US1] Verify response time < 200ms for authenticated users

## Completed Features Summary

✅ **Config Generation**: Three experience levels with distinct configs  
✅ **User Lookup**: Fast database query to get user's experience level  
✅ **Default Handling**: Graceful defaults for unauthenticated users and missing profiles  
✅ **Fast Response**: Config retrieval < 200ms  
✅ **Error Handling**: Database errors don't break the endpoint

**All user stories (US1, US2) are complete and independently testable.**

