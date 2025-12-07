import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import enum

# Load .env file from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("⚠️  WARNING: DATABASE_URL environment variable is not set")
    print("   Some features may not work. Please set DATABASE_URL in backend/.env")
    # Use a placeholder URL to allow the app to start
    DATABASE_URL = "postgresql://placeholder:placeholder@localhost/placeholder"
else:
    # Clean up DATABASE_URL - remove any extra characters, quotes, or command prefixes
    DATABASE_URL = DATABASE_URL.strip()
    # Remove 'psql' prefix if present
    if DATABASE_URL.startswith('psql '):
        DATABASE_URL = DATABASE_URL[5:].strip()
    # Remove single or double quotes
    DATABASE_URL = DATABASE_URL.strip("'\"")
    # Remove any trailing quotes or commands
    if DATABASE_URL.endswith("'"):
        DATABASE_URL = DATABASE_URL[:-1]
    if DATABASE_URL.endswith('"'):
        DATABASE_URL = DATABASE_URL[:-1]
    DATABASE_URL = DATABASE_URL.strip()

# Only create engine if DATABASE_URL is valid (not placeholder)
if DATABASE_URL and DATABASE_URL != "postgresql://placeholder:placeholder@localhost/placeholder":
    try:
        engine = create_engine(DATABASE_URL)
    except Exception as e:
        print(f"⚠️  WARNING: Could not create database engine: {e}")
        print("   Database features will not work")
        engine = None
else:
    engine = None
# Only create sessionmaker if engine exists
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    SessionLocal = None
Base = declarative_base()

class ExperienceLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Language(str, enum.Enum):
    EN = "en"
    UR = "ur"

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(String, primary_key=True)
    # user_id is legacy/redundant if we have email, but keeping for compatibility
    user_id = Column(String, nullable=False) 
    email = Column(String, unique=True, nullable=True) # Added email
    password_hash = Column(String, nullable=True)      # Added password hash
    name = Column(String, nullable=True)               # Added name
    
    software_background = Column(Text)
    hardware_background = Column(Text)
    experience_level = Column(Enum(ExperienceLevel), default=ExperienceLevel.BEGINNER)
    preferred_language = Column(Enum(Language), default=Language.EN)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    context = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ContentChunk(Base):
    __tablename__ = "content_chunks"
    
    id = Column(String, primary_key=True)
    content = Column(Text, nullable=False)
    module = Column(String(50))
    section = Column(String(100))
    embedding_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Translation(Base):
    __tablename__ = "translations"
    
    id = Column(String, primary_key=True)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    language = Column(String(10), nullable=False)
    module = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

async def init_db():
    """Initialize database tables"""
    if engine is None:
        raise Exception("Database engine not configured. Please set DATABASE_URL in .env file")
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    if SessionLocal is None:
        return None
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def save_chat_history(user_id: str, message: str, response: str, context: str = None):
    """Save chat history to database"""
    if SessionLocal is None:
        print("⚠️  Database not configured, skipping chat history save")
        return
    db = SessionLocal()
    try:
        import uuid
        chat_entry = ChatHistory(
            id=str(uuid.uuid4()),
            user_id=user_id,
            message=message,
            response=response,
            context=context
        )
        db.add(chat_entry)
        db.commit()
    except Exception as e:
        print(f"Error saving chat history: {e}")
        db.rollback()
    finally:
        db.close()
