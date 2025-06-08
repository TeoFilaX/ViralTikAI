# backend/app/services/transcription.py

import whisper
from fastapi import HTTPException

# Cargar el modelo Whisper una sola vez (podrías configurarlo para distintos tamaños)
_modelo_whisper = None

def _cargar_modelo(model_name: str = "base"):
    """
    Carga el modelo Whisper (global) si no está cargado aún.
    """
    global _modelo_whisper
    if _modelo_whisper is None:
        try:
            _modelo_whisper = whisper.load_model(model_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"No se pudo cargar Whisper: {e}")
    return _modelo_whisper

def transcribir(ruta_audio: str, model_name: str = "base") -> str:
    """
    Dada la ruta a un archivo de audio (WAV, 16kHz mono) usa Whisper para transcribir.
    Retorna la transcripción en texto.
    """
    modelo = _cargar_modelo(model_name)
    try:
        resultado = modelo.transcribe(ruta_audio)
        return resultado.get("text", "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en transcripción con Whisper: {e}")
