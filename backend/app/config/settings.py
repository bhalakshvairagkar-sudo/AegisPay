"""
Backend Application Settings
"""

from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "AegisPay Defense Lab"
    version: str = "2026.1"
    debug: bool = True
    default_seed: int = 42
    trained_models_dir: str = "backend/trained_models"
    experiments_dir: str = "backend/experiments"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]


settings = Settings()
