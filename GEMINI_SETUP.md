# Gemini 3 Pro Setup

## ✅ Updated to Use Gemini 3 Pro

The backend now uses **Gemini 3 Pro** (via the new `google-genai` SDK) for:
- ✅ Chat responses (state-of-the-art reasoning)
- ✅ Translations (intelligent multilingual support)

OpenAI is still used for:
- ✅ Embeddings (`text-embedding-3-small`)

## Setup

1. **Get Gemini API Key:**
   - Go to: https://aistudio.google.com/app/apikey
   - Create a new API key
   - Copy the key

2. **Add to `.env` file:**
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Install dependencies:**
   ```bash
   cd backend
   source venv/bin/activate
   pip install google-genai google-generativeai
   ```

4. **Restart the server:**
   ```bash
   ./START_SERVER.sh
   ```

## Model Used

- **Gemini 3 Pro Preview** (`gemini-3-pro-preview`) for chat
  - Configured with `thinking_level="high"` for complex reasoning
- **Gemini 3 Pro** or **Flash** for translations
- **OpenAI text-embedding-3-small** for embeddings

## Troubleshooting

If you see API errors:
- Ensure your API key has access to `gemini-3-pro-preview`.
- Check if you are in a supported region.
- The system will automatically fall back to older models (`gemini-1.5-flash`, etc.) if Gemini 3 is unavailable.

## Environment Variables

```env
# For embeddings (vector search)
OPENAI_API_KEY=sk-...

# For chat and translations
GEMINI_API_KEY=AIzaSyA...
```

Both are required for full functionality!
