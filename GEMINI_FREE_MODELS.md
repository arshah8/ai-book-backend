# Gemini Models Guide

## ✅ Model Priority

The backend is configured to use the best available model:

1. **gemini-3-pro-preview** (Best Quality - Paid/Preview)
   - State-of-the-art reasoning
   - Requires API access/credits
   - Uses `thinking_level="high"`

2. **gemini-1.5-flash** (Free Tier Fallback)
   - Fast and free (within limits)
   - Good for general tasks
   - Fallback if Gemini 3 is unavailable

3. **gemini-pro** (Legacy Free Tier)
   - Standard legacy model
   - Widely compatible

## Test Available Models

Run this to see what models your API key has access to:

```bash
cd backend
source venv/bin/activate
python3 LIST_MODELS.py
```

## Configuration

No manual changes needed. The system automatically detects if Gemini 3 is available and falls back gracefully if not.
