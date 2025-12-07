from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: Optional[str] = None
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

class TranslateRequest(BaseModel):
    text: str
    language: str = "ur"  # "ur" for Urdu, "en" for English
    module: Optional[str] = None

class TranslateResponse(BaseModel):
    translated_text: str

class PersonalizationConfig(BaseModel):
    show_advanced_topics: bool
    show_code_examples: bool
    code_complexity: str  # "simple", "standard", "advanced"
    explanation_depth: str  # "basic", "detailed", "comprehensive"

