from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
# Note: Install PyJWT package: pip install PyJWT
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import uuid

# Load .env file from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

from app.database import get_db, UserProfile, ExperienceLevel

router = APIRouter()
security = HTTPBearer(auto_error=False)

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

class User(BaseModel):
    id: str
    email: str
    name: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

# For optional authentication (allows None)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """Get current user from JWT token (optional)"""
    if credentials is None:
        return None
    token = credentials.credentials
    payload = verify_token(token)
    return payload

# Auth request/response models
class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    software_background: Optional[str] = None
    hardware_background: Optional[str] = None
    experience_level: Optional[str] = "beginner"

class SigninRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """User signup with background questionnaire"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")

    # Check if user already exists
    existing_user = db.query(UserProfile).filter(UserProfile.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    profile_id = str(uuid.uuid4())
    hashed_password = get_password_hash(request.password)
    
    # Validate experience level enum
    try:
        exp_level = ExperienceLevel(request.experience_level)
    except ValueError:
        exp_level = ExperienceLevel.BEGINNER

    new_user = UserProfile(
        id=profile_id,
        user_id=profile_id, # Use same ID for user_id for now
        email=request.email,
        password_hash=hashed_password,
        name=request.name,
        software_background=request.software_background,
        hardware_background=request.hardware_background,
        experience_level=exp_level
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    # Create JWT token
    user_data = {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
        "experience_level": new_user.experience_level.value if hasattr(new_user.experience_level, 'value') else new_user.experience_level
    }
    
    token = create_access_token({"id": new_user.id, "email": new_user.email})
    
    return AuthResponse(
        access_token=token,
        user=user_data
    )

@router.post("/signin", response_model=AuthResponse)
async def signin(request: SigninRequest, db: Session = Depends(get_db)):
    """User signin"""
    if not db:
         raise HTTPException(status_code=503, detail="Database not available")

    # Check if user exists
    user = db.query(UserProfile).filter(UserProfile.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not user.password_hash or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create JWT token
    user_data = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "experience_level": user.experience_level.value if hasattr(user.experience_level, 'value') else user.experience_level
    }
    
    token = create_access_token({"id": user.id, "email": user.email})
    
    return AuthResponse(
        access_token=token,
        user=user_data
    )
