# Fixing Installation Issues

## Issue: better-auth version not found

The `better-auth==0.1.0` package doesn't exist. We've removed it from requirements.txt since we're using JWT authentication directly.

## Quick Fix

1. **Upgrade pip first:**
   ```bash
   python3 -m pip install --upgrade pip
   ```

2. **Install requirements:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **If you still get errors, install manually:**
   ```bash
   pip3 install fastapi uvicorn[standard] python-dotenv openai qdrant-client psycopg2-binary sqlalchemy alembic pydantic pydantic-settings python-multipart python-jose[cryptography] passlib[bcrypt] httpx
   ```

## Verify Installation

```bash
uvicorn --version
python3 -c "import fastapi; print('FastAPI installed')"
```

## Start the Server

```bash
uvicorn app.main:app --reload
```

