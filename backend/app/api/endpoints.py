# backend/app/api/endpoints.py
import uuid
import traceback               # ➜ Para imprimir trazas completas
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from ..services.transcription import transcribir
from ..services.video_analysis import analizar_video_completo
from ..models.schemas import TranscriptionResponse, AnalysisResponse
from ..utils.ffmpeg_utils import extraer_audio

router = APIRouter(prefix="/api", tags=["ViralBoostAI"])

# Carpeta temporal para guardar uploads
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)


@router.post("/transcribe", response_model=TranscriptionResponse)
async def endpoint_transcribir_video(
    background_tasks: BackgroundTasks,
    video_file: UploadFile = File(...)
):
    """
    Recibe un archivo de video, extrae el audio, lo transcribe y devuelve la transcripción.
    """
    if not video_file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        raise HTTPException(status_code=415, detail="Formato de video no soportado.")

    temp_id = uuid.uuid4().hex
    video_path = TEMP_DIR / f"{temp_id}_{video_file.filename}"
    audio_path = TEMP_DIR / f"{temp_id}.wav"

    with open(video_path, "wb") as f:
        f.write(await video_file.read())

    try:
        extraer_audio(str(video_path), str(audio_path))
        texto = transcribir(str(audio_path))
    except Exception as e:
        traceback.print_exc()         # ➜ Traza completa en terminal
        if video_path.exists():
            video_path.unlink()
        if audio_path.exists():
            audio_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error al procesar: {e}")

    background_tasks.add_task(lambda p: Path(p).unlink(), str(video_path))
    background_tasks.add_task(lambda p: Path(p).unlink(), str(audio_path))

    return TranscriptionResponse(
        filename=video_file.filename,
        transcription=texto
    )


@router.post("/analyze", response_model=AnalysisResponse)
async def endpoint_analizar_video(
    background_tasks: BackgroundTasks,
    video_file: UploadFile = File(...)
):
    """
    Recibe un video, orquesta extracción, transcripción y análisis LLM completo.
    """
    if not video_file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        raise HTTPException(status_code=415, detail="Formato de video no soportado.")

    temp_id = uuid.uuid4().hex
    video_path = TEMP_DIR / f"{temp_id}_{video_file.filename}"
    audio_path = TEMP_DIR / f"{temp_id}.wav"

    with open(video_path, "wb") as f:
        f.write(await video_file.read())

    try:
        extraer_audio(str(video_path), str(audio_path))
        resultado = analizar_video_completo(str(video_path), str(audio_path))
    except Exception as e:
        traceback.print_exc()         # ➜ Traza completa en terminal
        if video_path.exists():
            video_path.unlink()
        if audio_path.exists():
            audio_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error en análisis: {e}")

    background_tasks.add_task(lambda p: Path(p).unlink(), str(video_path))
    background_tasks.add_task(lambda p: Path(p).unlink(), str(audio_path))

    return JSONResponse(content=resultado)


@router.get("/health", status_code=200)
async def health_check():
    """
    Endpoint simple para monitoreo.
    """
    return {"status": "ok", "detail": "ViralBoostAI backend saludable"}
