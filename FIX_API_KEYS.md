# Fixing API Key Issues

## Problem

The server crashes on startup because:
1. OpenAI client is initialized at import time without checking if API key exists
2. You're using Gemini for chat, but OpenAI is still needed for embeddings

## Solution

I've made the code more resilient:
- ✅ OpenAI client is now lazy-loaded (only when needed)
- ✅ Fallback embedding if OpenAI key is missing
- ✅ Gemini client configured only when needed
- ✅ Server can start even if some API keys are missing

## Required API Keys

### For Full Functionality:

1. **GEMINI_API_KEY** (Required for chat and translations)
   - Get from: https://aistudio.google.com/app/apikey
   - Add to `backend/.env`:
   ```env
   GEMINI_API_KEY=AIzaSyA7...your_key_here
   ```

2. **OPENAI_API_KEY** (Required for embeddings/vector search)
   - Get from: https://platform.openai.com/api-keys
   - Add to `backend/.env`:
   ```env
   OPENAI_API_KEY=sk-...your_key_here
   ```

### Minimum Setup (Chat works, but no vector search):

If you only have Gemini key:
- ✅ Chat will work
- ✅ Translations will work
- ⚠️ Vector search will use fallback (less accurate)

## Your .env File Should Have:

```env
# Gemini (for chat and translations)
GEMINI_API_KEY=AIzaSyA7...your_gemini_key

# OpenAI (for embeddings)
OPENAI_API_KEY=sk-...your_openai_key

# Other keys...
QDRANT_URL=https://...
QDRANT_API_KEY=...
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
```

## Restart Server

After updating `.env`:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

The server should now start successfully even if some keys are missing (with warnings).

