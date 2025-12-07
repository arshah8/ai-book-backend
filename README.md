---
title: AI Textbook Backend API
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: 3
app_port: 8000
---

# Physical AI Textbook - FastAPI Backend

A production-ready FastAPI backend for the Physical AI & Humanoid Robotics textbook.

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp env.example .env
# Edit .env with your API keys

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 API Endpoints

- `GET /health` - Health check
- `POST /api/chat` - RAG chatbot endpoint
- `POST /api/translate` - Translate content to Urdu
- `GET /api/personalize` - Get user personalization settings
- `POST /auth/signup` - User signup
- `POST /auth/signin` - User signin

## 🔑 Environment Variables

Set these in **Hugging Face Space Settings → Variables**:

- `GEMINI_API_KEY` - Gemini API key (required)
- `QDRANT_URL` - Qdrant Cloud URL (required)
- `QDRANT_API_KEY` - Qdrant API key (required)
- `DATABASE_URL` - Neon PostgreSQL connection string (required)
- `BETTER_AUTH_SECRET` - JWT secret key (required)

## 🚢 Deployment on Hugging Face

1. **Create Space**: Go to [huggingface.co/spaces](https://huggingface.co/spaces) → New Space → Select **Docker**
2. **Push Code**: Clone the space and push your code
3. **Set Variables**: Add all environment variables in Space Settings
4. **Access API**: `https://YOUR_USERNAME-ai-textbook-backend.hf.space`

## 📝 License

MIT License - Hackathon Project
