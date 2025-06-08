# backend/app/utils/ffmpeg_utils.py

import subprocess
import os
from fastapi import HTTPException

def extraer_audio(video_path: str, output_audio: str) -> None:
    """
    Usa ffmpeg para extraer la pista de audio de un video:
      - video_path: ruta al archivo de video.
      - output_audio: ruta de salida (WAV mono, 16 kHz).
    Lanza HTTPException si ffmpeg falla.
    """
    # Comando básico para convertir a WAV mono 16kHz
    comando = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # no incluir video
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio
    ]
    try:
        subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar ffmpeg: {e}")

def convertir_video_formato(
    video_path: str,
    output_path: str,
    codec: str = "libx264",
    bitrate: str = "1M"
) -> None:
    """
    (Opcional) Convierte el video a un formato estándar (H.264 MP4) para asegurar compatibilidad.
    """
    comando = [
        "ffmpeg",
        "-i", video_path,
        "-c:v", codec,
        "-b:v", bitrate,
        "-c:a", "aac",
        "-strict", "experimental",
        output_path
    ]
    try:
        subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error al convertir video: {e}")
