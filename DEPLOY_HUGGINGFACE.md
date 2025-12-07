# Step-by-Step Guide: Deploy to Hugging Face Spaces

## Prerequisites
- Hugging Face account (free at [huggingface.co](https://huggingface.co))
- Git installed
- All your API keys ready

## Step 1: Create Hugging Face Space

1. Go to [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"New Space"** button
3. Fill in:
   - **Space name**: `ai-textbook-backend` (or your choice)
   - **SDK**: Select **"Docker"**
   - **Hardware**: Free CPU (or upgrade if needed)
   - **Visibility**: Public or Private
4. Click **"Create Space"**

## Step 2: Clone Your Space Repository

After creating, Hugging Face will show you commands. Run:

```bash
# Install Hugging Face CLI (if not installed)
pip install huggingface_hub

# Login to Hugging Face
huggingface-cli login
# Enter your token (get it from https://huggingface.co/settings/tokens)

# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-textbook-backend
cd ai-textbook-backend
```

**Replace `YOUR_USERNAME` with your actual Hugging Face username!**

## Step 3: Copy Your Backend Files

```bash
# Copy all files from your backend folder
cp -r /path/to/ai-book-backend/* .

# Or if you're in the parent directory:
cp -r ai-book-backend/* ai-textbook-backend/
```

**Important files to copy:**
- `Dockerfile` ✅
- `requirements.txt` ✅
- `app/` folder ✅
- `scripts/` folder ✅
- `README.md` ✅

**Do NOT copy:**
- `.env` (sensitive - use Space variables instead)
- `venv/` (not needed in Docker)
- `.git/` (already exists in the space repo)

## Step 4: Commit and Push

```bash
# Add all files
git add .

# Commit
git commit -m "Initial deployment: FastAPI backend"

# Push to Hugging Face
git push
```

## Step 5: Set Environment Variables

1. Go to your Space page on Hugging Face
2. Click **"Settings"** tab
3. Scroll to **"Variables and secrets"**
4. Add each variable:

   | Variable Name | Value |
   |--------------|-------|
   | `GEMINI_API_KEY` | Your Gemini API key |
   | `QDRANT_URL` | Your Qdrant URL |
   | `QDRANT_API_KEY` | Your Qdrant API key |
   | `DATABASE_URL` | Your Neon PostgreSQL URL |
   | `BETTER_AUTH_SECRET` | Your JWT secret |

5. Click **"Save"** after adding each variable

## Step 6: Wait for Build

- Hugging Face will automatically build your Docker image
- This takes 5-10 minutes the first time
- Watch the build logs in the Space page

## Step 7: Test Your API

Once deployed, your API will be at:
```
https://YOUR_USERNAME-ai-textbook-backend.hf.space
```

Test it:
```bash
curl https://YOUR_USERNAME-ai-textbook-backend.hf.space/health
```

Should return: `{"status":"healthy"}`

## Troubleshooting

### Build Fails
- Check the build logs in Hugging Face
- Make sure `Dockerfile` is in the root directory
- Verify `requirements.txt` exists

### API Not Responding
- Check environment variables are set correctly
- Look at the Space logs
- Verify the port is 8000 (or check Space settings)

### Database Connection Errors
- Verify `DATABASE_URL` is correct
- Make sure it uses the pooler URL from Neon

## Next Steps

1. Update your frontend's `NEXT_PUBLIC_API_URL` to point to your Hugging Face Space URL
2. Test all endpoints
3. Share your Space URL with others!

