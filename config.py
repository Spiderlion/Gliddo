# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    SUPABASE_URL: str
    SUPABASE_KEY: str
    TIMEZONE: str = "Asia/Kolkata"
    
    class Config:
        env_file = ".env"

# Initialize settings
settings = Settings()