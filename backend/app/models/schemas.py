# backend/app/models/schemas.py

from pydantic import BaseModel
from typing import List, Optional

class TranscriptionResponse(BaseModel):
    """
    Esquema de respuesta para /api/transcribe:
      - filename: nombre original del archivo.
      - transcription: texto resultante de Whisper.
    """
    filename: str
    transcription: str

class AnalysisResponse(BaseModel):
    """
    Esquema de respuesta para /api/analyze:
      - transcription: texto transcrito completo.
      - analysis: puede ser un objeto con claves como 'summary', 'hashtags', 'tips' o texto sin parsear.
    """
    transcription: str
    analysis: dict

class ErrorResponse(BaseModel):
    """
    Esquema genérico de error.
    """
    detail: Optional[str] = None
