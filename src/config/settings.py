import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # MongoDB Settings
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    master_db_name: str = os.getenv("MASTER_DB_NAME", "organization_master")
    
    # JWT Settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Application Settings
    app_name: str = "Organization Management Service"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Security
    bcrypt_rounds: int = 12
    
    class Config:
        env_file = ".env"

settings = Settings()