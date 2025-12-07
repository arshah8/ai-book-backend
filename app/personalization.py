from app.database import UserProfile, SessionLocal, ExperienceLevel
from typing import Dict

async def get_user_personalization(user_id: str) -> Dict:
    """Get personalization config for user"""
    db = SessionLocal()
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == user_id
        ).first()
        
        if not profile:
            return get_default_config()
        
        experience_level = profile.experience_level or ExperienceLevel.BEGINNER
        
        return get_config_for_level(experience_level)
    except Exception as e:
        print(f"Error getting personalization: {e}")
        return get_default_config()
    finally:
        db.close()

def get_config_for_level(level: ExperienceLevel) -> Dict:
    """Get config based on experience level"""
    if level == ExperienceLevel.BEGINNER:
        return {
            "show_advanced_topics": False,
            "show_code_examples": True,
            "code_complexity": "simple",
            "explanation_depth": "detailed"
        }
    elif level == ExperienceLevel.INTERMEDIATE:
        return {
            "show_advanced_topics": True,
            "show_code_examples": True,
            "code_complexity": "standard",
            "explanation_depth": "detailed"
        }
    else:  # ADVANCED
        return {
            "show_advanced_topics": True,
            "show_code_examples": True,
            "code_complexity": "advanced",
            "explanation_depth": "comprehensive"
        }

def get_default_config() -> Dict:
    """Get default personalization config"""
    return {
        "show_advanced_topics": True,
        "show_code_examples": True,
        "code_complexity": "standard",
        "explanation_depth": "detailed"
    }

