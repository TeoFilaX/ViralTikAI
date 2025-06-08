# backend/app/utils/config.py

import os
from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """
    Carga y valida variables de entorno necesarias para el backend.
    """
    # API Key de OpenAI (para GPT-4)
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    # Ruta al modelo Mistral local (GGUF)
    MISTRAL_MODEL_PATH: str = Field("", env="/Users/christianmonzon/Desktop/ViralBoostAI/backend/app/models/Mistral-7B-v0.1/mistral-7b-instruct-auto.gguf")
    # Directorio temporal para guardar videos y audios
    TEMP_DIR: str = Field("temp", env="TEMP_DIR")
    # Otros parámetros (si se requieren más)
    # MAX_VIDEO_SIZE_MB: int = Field(100, env="MAX_VIDEO_SIZE_MB")
    # CORS_ALLOWED_ORIGINS: str = Field("*", env="CORS_ALLOWED_ORIGINS")

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../.env")
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """
    Devuelve una instancia cacheada de Settings, para usar en toda la app.
    """
    return Settings()
