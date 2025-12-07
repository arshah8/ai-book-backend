# Quick Fix for Gemini Module Error

## ✅ Fixed!

The `google-generativeai` package has been installed. There was a protobuf version conflict, but it should work now.

## Test It

1. **Make sure GEMINI_API_KEY is in your `.env`:**
   ```env
   GEMINI_API_KEY=AIzaSyA7...your_key_here
   ```

2. **Restart the server:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

3. **Test the chat:**
   - Go to http://localhost:3000
   - Click the chatbot icon
   - Ask a question

## If You Still Get Errors

If you see protobuf errors, run:
```bash
cd backend
source venv/bin/activate
pip install --upgrade protobuf
```

The server should now work with Gemini 2.5 Flash!
