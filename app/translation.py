from app.database import Translation, SessionLocal
from app.openai_client import translate_text as openai_translate
from sqlalchemy import and_
from typing import Optional

async def get_cached_translation(original_text: str, language: str) -> Optional[str]:
    """Get cached translation from database"""
    if SessionLocal is None:
        return None
    db = SessionLocal()
    try:
        translation = db.query(Translation).filter(
            and_(
                Translation.original_text == original_text,
                Translation.language == language
            )
        ).first()
        return translation.translated_text if translation else None
    except Exception as e:
        print(f"Error getting cached translation: {e}")
        return None
    finally:
        db.close()

async def cache_translation(
    original_text: str,
    translated_text: str,
    language: str,
    module: Optional[str] = None
):
    """Cache translation in database"""
    if SessionLocal is None:
        return
    db = SessionLocal()
    try:
        import uuid
        translation = Translation(
            id=str(uuid.uuid4()),
            original_text=original_text,
            translated_text=translated_text,
            language=language,
            module=module
        )
        db.add(translation)
        db.commit()
    except Exception as e:
        print(f"Error caching translation: {e}")
        db.rollback()
    finally:
        db.close()
