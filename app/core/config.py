from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

class Settings(BaseSettings):
    """
    Configuration settings for the Personalized Learning System.
    Reads values from the environment using Pydantic.
    """

    # Project Settings
    PROJECT_NAME: str = "Personalized Learning System"

    # API Keys
    OPENAI_API_KEY: str
    GOOGLE_API_KEY: str
    GOOGLE_CSE_ID: str
    GOOGLE_CUSTOM_API_KEY: str
    SERPER_API_KEY: str
    FIRECRAWL_API_KEY: str

    # LangSmith Settings
    LANGSMITH_TRACING: bool
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str

    # Security
    JWT_SECRET_KEY: str

    # Database (Optional)
    DATABASE_URL: str = "sqlite:///./database.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

@lru_cache
def get_settings():
    """Load environment variables dynamically without restarting the system."""
    load_dotenv(override=True)
    return Settings()

settings = get_settings()
