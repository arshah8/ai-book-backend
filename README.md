# Physical AI Textbook - FastAPI Backend

A production-ready FastAPI backend for the Physical AI & Humanoid Robotics textbook, featuring:
- **Gemini 3 Pro** for AI chat responses
- **Gemini Embeddings** for vector search
- **Qdrant Cloud** for vector database
- **Neon PostgreSQL** for user data and chat history
- **JWT Authentication** with bcrypt password hashing

## 🚀 Quick Start

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
cp env.example .env
# Edit .env with your API keys (see below)
```

### 4. Seed Qdrant Vector Database
```bash
python scripts/seed_vectors.py
```

### 5. Start the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the convenience script:
```bash
./START_SERVER.sh
```

## 📋 API Endpoints

### Chat
- `POST /api/chat` - RAG chatbot endpoint (requires auth token for chat history)

### Translation
- `POST /api/translate` - Translate content to Urdu (cached in database)

### Personalization
- `GET /api/personalize` - Get user personalization settings (based on experience level)

### Auth
- `POST /auth/signup` - User signup with background questionnaire
- `POST /auth/signin` - User signin

### Health
- `GET /health` - Health check endpoint
- `GET /` - API status

## 🔑 Environment Variables

Required environment variables (set in `.env`):

```env
# Gemini API (for chat and embeddings)
GEMINI_API_KEY=your_gemini_api_key_here

# Qdrant Cloud (vector database)
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key

# Neon PostgreSQL (user data and chat history)
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# JWT Secret (generate with: openssl rand -hex 32)
BETTER_AUTH_SECRET=your_secret_key_here
```

## 🏗️ Architecture

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **Qdrant**: Vector similarity search
- **Gemini 3 Pro**: State-of-the-art AI reasoning
- **Neon Postgres**: Serverless PostgreSQL with connection pooling

## 📦 Project Structure

```
ai-book-backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── auth.py           # JWT authentication
│   ├── database.py       # SQLAlchemy models and connection
│   ├── gemini_client.py  # Gemini 3 Pro integration
│   ├── openai_client.py  # Gemini embeddings (legacy name)
│   ├── qdrant_client.py  # Qdrant vector database
│   ├── translation.py   # Translation with caching
│   └── personalization.py # User content personalization
├── scripts/
│   └── seed_vectors.py   # Seed Qdrant with book content
├── requirements.txt      # Python dependencies
├── env.example           # Environment variable template
└── README.md            # This file
```

## 🚢 Deployment

### Railway
1. Connect your GitHub repo
2. Set root directory to `ai-book-backend`
3. Add environment variables
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Render
1. New Web Service
2. Connect GitHub repo
3. Root directory: `ai-book-backend`
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

## 🔧 Troubleshooting

### Database Connection Issues
- Ensure `DATABASE_URL` uses the **pooler** URL from Neon (ends with `-pooler`)
- Connection pooling is configured automatically for Neon

### Qdrant Connection
- Verify `QDRANT_URL` doesn't have typos (e.g., `hhttps` → `https`)
- Check API key is valid

### Gemini API
- Free tier has rate limits; system automatically falls back to other models
- Check quota at: https://ai.dev/usage

## 📝 License

MIT License - Hackathon Project
