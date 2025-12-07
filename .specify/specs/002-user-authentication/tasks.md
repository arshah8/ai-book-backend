# Tasks: User Authentication System

**Input**: `spec.md` and `plan.md` under `.specify/specs/002-user-authentication/`  
**Prerequisites**: Database infrastructure (005-database-infrastructure) must be in place.

## Phase 1: Database Models (DONE)

- [x] T001 [P] Create `UserProfile` model in `app/database.py` with email, password_hash, name fields
- [x] T002 [P] Add `ExperienceLevel` enum (BEGINNER, INTERMEDIATE, ADVANCED) to database models
- [x] T003 [P] Add background questionnaire fields: software_background, hardware_background, experience_level
- [x] T004 [P] Ensure `UserProfile` table is created in `init_db()` function

## Phase 2: Password Hashing & JWT (DONE)

- [x] T010 [P] Install and configure `passlib[bcrypt]` for password hashing
- [x] T011 [P] Implement `get_password_hash()` function using CryptContext
- [x] T012 [P] Implement `verify_password()` function for password verification
- [x] T013 [P] Install and configure `PyJWT` for JWT token handling
- [x] T014 [P] Implement `create_access_token()` with 7-day expiration
- [x] T015 [P] Implement `verify_token()` for JWT validation
- [x] T016 [P] Configure JWT secret via `BETTER_AUTH_SECRET` environment variable

## Phase 3: Authentication Dependencies (DONE)

- [x] T020 [P] Implement `get_current_user()` dependency for required authentication
- [x] T021 [P] Implement `get_current_user_optional()` dependency for optional authentication
- [x] T022 [P] Add HTTPBearer security scheme for token extraction
- [x] T023 [P] Handle token expiration and invalid token errors

## Phase 4: Signup Endpoint (DONE)

- [x] T030 [US1] Create `SignupRequest` model with email, password, name, background fields
- [x] T031 [US1] Create `POST /auth/signup` endpoint in `app/auth.py`
- [x] T032 [US1] Validate email uniqueness (check existing users in database)
- [x] T033 [US1] Hash password before storing in database
- [x] T034 [US1] Create user profile with all provided information
- [x] T035 [US1] Generate JWT token and return in `AuthResponse`
- [x] T036 [US1] Handle duplicate email error (400 Bad Request)
- [x] T037 [US1] Handle database errors gracefully

## Phase 5: Signin Endpoint (DONE)

- [x] T040 [US2] Create `SigninRequest` model with email and password
- [x] T041 [US2] Create `POST /auth/signin` endpoint in `app/auth.py`
- [x] T042 [US2] Verify user exists in database
- [x] T043 [US2] Verify password using `verify_password()`
- [x] T044 [US2] Generate JWT token on successful authentication
- [x] T045 [US2] Return user data and token in `AuthResponse`
- [x] T046 [US2] Handle invalid credentials (401 Unauthorized)
- [x] T047 [US2] Handle database unavailability (503 Service Unavailable)

## Phase 6: Integration & Testing (DONE)

- [x] T050 [US3] Create FastAPI router in `app/auth.py` with `/signup` and `/signin` routes
- [x] T051 [US3] Include auth router in `app/main.py` at `/auth` prefix
- [x] T052 [US3] Add optional authentication to `/api/chat` endpoint using `get_current_user_optional`
- [x] T053 [US3] Test signup flow with valid and invalid data
- [x] T054 [US3] Test signin flow with valid and invalid credentials
- [x] T055 [US3] Test JWT token validation on authenticated endpoints
- [x] T056 [US3] Test optional authentication (endpoints work with or without token)

## Completed Features Summary

✅ **Password Security**: All passwords hashed with bcrypt before storage  
✅ **JWT Tokens**: 7-day expiration, validated on every authenticated request  
✅ **User Profiles**: Complete user information including background questionnaire  
✅ **Optional Auth**: Public features work without authentication, enhanced features require it  
✅ **Error Handling**: Clear error messages for all failure scenarios

**All user stories (US1, US2, US3) are complete and independently testable.**

