# Gemini Models - Free Tier

## ✅ Updated to Use Free Tier Models

The code now uses **free tier models** that work with your newly created API key.

## Free Tier Models Available

1. **gemini-1.5-flash** ✅ (Primary - Now Using)
   - Fast and efficient
   - Free tier: 15 requests per minute
   - Best for most use cases

2. **gemini-pro** ✅ (Fallback)
   - Standard model
   - Free tier: 60 requests per minute
   - More capable but slower

3. **gemini-2.0-flash-exp** ❌ (Paid Tier Only)
   - Requires paid tier
   - Not available on free tier
   - Removed from code

## What Changed

- ✅ Primary model: `gemini-1.5-flash` (free tier)
- ✅ Fallback: `gemini-pro` (free tier)
- ❌ Removed: `gemini-2.0-flash-exp` (paid tier only)

## Free Tier Limits

- **gemini-1.5-flash**: 15 requests/minute
- **gemini-pro**: 60 requests/minute

## Your Setup

Since you just created the API key from Google AI Studio:
1. ✅ Your key should work immediately
2. ✅ Free tier is active by default
3. ✅ No billing required

## Restart Server

After the code update, restart:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

The chat should now work with the free tier!

## Verify Your API Key

Make sure in `backend/.env`:
```env
GEMINI_API_KEY=AIzaSyA...your_key_from_google_ai_studio
```

The key should start with `AIza` and come from:
https://aistudio.google.com/app/apikey

