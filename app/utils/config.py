import os
from typing import Optional, Dict, Any
from pydantic import BaseSettings, validator, PostgresDsn
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Application settings
    APP_NAME: str = "AI Velocity Dashboard"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # Database settings
    POSTGRES_SERVER: Optional[str] = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB", "aivelocity")
    DATABASE_URI: Optional[PostgresDsn] = None
    
    # GitHub settings
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    GITHUB_ORG: Optional[str] = os.getenv("GITHUB_ORG")
    
    # LangSmith settings
    LANGSMITH_API_KEY: Optional[str] = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: Optional[str] = os.getenv("LANGSMITH_PROJECT")
    
    # AWS settings (for future use)
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: Optional[str] = os.getenv("AWS_REGION", "us-west-2")
    
    # Sentry settings (for error tracking)
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
    
    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Assemble the database connection string."""
        if isinstance(v, str):
            return v
            
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        """Assemble CORS origins."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

# Create settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the application settings."""
    return settings

def is_production() -> bool:
    """Check if the application is running in production mode."""
    return settings.ENVIRONMENT == "production"

def is_development() -> bool:
    """Check if the application is running in development mode."""
    return settings.ENVIRONMENT == "development"

def is_testing() -> bool:
    """Check if the application is running in test mode."""
    return settings.ENVIRONMENT == "test"
