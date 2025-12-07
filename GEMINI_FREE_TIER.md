# Using Gemini Free Tier

## ✅ Fixed: Now Using Free Tier Model

I've updated the code to use **`gemini-1.5-flash`** which is available on the free tier.

## Why the Error Happened

- `gemini-2.0-flash-exp` requires a **paid tier** (quota limit: 0 for free tier)
- `gemini-1.5-flash` is available on the **free tier**

## Models Available on Free Tier

1. ✅ **gemini-1.5-flash** - Fast, free tier model (now using this)
2. ✅ **gemini-pro** - Standard model, also free tier
3. ❌ **gemini-2.0-flash-exp** - Requires paid tier

## What Changed

The code now:
- Uses `gemini-1.5-flash` as the primary model
- Falls back to `gemini-pro` if flash is unavailable
- No longer tries `gemini-2.0-flash-exp` (paid tier only)

## Free Tier Limits

According to Google's free tier:
- **gemini-1.5-flash**: 15 requests per minute
- **gemini-pro**: 60 requests per minute

## Restart Server

After the code update, restart your server:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

The chat should now work with the free tier model!

## Check Your API Key

Make sure your `GEMINI_API_KEY` in `backend/.env` is from:
- https://aistudio.google.com/app/apikey
- Should start with `AIza...`

The free tier should work immediately after creating the API key.

