# Fixing DATABASE_URL Format Issue

## Problem
The DATABASE_URL in your `.env` file has extra characters:
```
psql 'postgresql://...'
```

SQLAlchemy can't parse this because it includes the `psql` command prefix and quotes.

## Solution

I've updated the code to automatically clean the DATABASE_URL, but you should also fix your `.env` file.

### Fix Your .env File

Edit `backend/.env` and make sure `DATABASE_URL` looks like this:

```env
DATABASE_URL=postgresql://neondb_owner:npg_dj4gCrkz7FKH@ep-curly-dust-a46qchg4-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

**Important:**
- ❌ NO `psql` prefix
- ❌ NO quotes around the URL
- ✅ Just the URL directly

### What I Fixed in Code

The code now automatically:
1. Strips whitespace
2. Removes `psql` prefix if present
3. Removes quotes
4. Validates the URL format

### Test

After fixing your `.env` file, restart the server:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

The server should now start successfully!

