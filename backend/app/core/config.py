from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Paper Reading Agent System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # AI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"  # Default model
    
    # Database Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "paper_reading_db"
    
    # Storage Configuration
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
