# Physical AI Textbook - FastAPI Backend

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run database migrations (if using Alembic):
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Chat
- `POST /api/chat` - RAG chatbot endpoint

### Translation
- `POST /api/translate` - Translate content to Urdu

### Personalization
- `GET /api/personalize` - Get user personalization settings

### Auth
- `POST /auth/signup` - User signup
- `POST /auth/signin` - User signin

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `DATABASE_URL` - Neon Postgres connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT tokens

