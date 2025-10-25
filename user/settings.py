from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App Info
    app_name: str = "CineMatch Users API"
    version: str = "1.0.0"
    description: str = "Microservicio de usuarios para CineMatch"
    
    # Database
    database_url: str = "postgresql://cinematch_user:cinematch_password@db:5432/cinematch_users"
    
    # JWT Configuration
    jwt_secret: str = "your_super_secret_jwt_key_change_this_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Security
    bcrypt_rounds: int = 12
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    debug: bool = False
    
    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instancia global de configuración
settings = Settings()