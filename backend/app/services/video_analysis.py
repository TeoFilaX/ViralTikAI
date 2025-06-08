# backend/app/services/video_analysis.py

from ..services.transcription import transcribir
from ..services.llm_client import generar_analisis_llm
from fastapi import HTTPException
import os

def analizar_video_completo(ruta_video: str, ruta_audio: str) -> dict:
    """
    Pipeline completo de análisis:
      1. Transcripción (ya tenemos ruta_audio).
      2. Generar prompt para LLM con la transcripción y datos básicos.
      3. Invocar LLM (OpenAI o local) para generar sugerencias de viralización.
    Retorna un diccionario con el análisis completo.
    """
    try:
        # 1) Transcribir
        texto = transcribir(ruta_audio)

        # 2) Preparar prompt dinámico
        prompt = (
            "Eres ViralBoostAI. A partir de esta transcripción de un video de TikTok, "
            "genera:\n"
            "1. Resumen breve del contenido.\n"
            "2. Lista de hashtags recomendados (entre 5 y 10).\n"
            "3. Sugerencias de optimización (título, descripción, horario de publicación).\n\n"
            f"Transcripción:\n\"\"\"\n{texto}\n\"\"\""
        )

        # 3) Invocar LLM para análisis usando Mistral local
        resultado_llm = generar_analisis_llm(prompt, modelo="mistral")

        # 4) Formatear resultado
        return {
            "transcription": texto,
            "analysis": resultado_llm
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en pipeline de análisis: {e}")
