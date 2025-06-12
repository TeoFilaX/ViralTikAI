from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from typing import List

# Directories
BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_ROOT.mkdir(exist_ok=True)

# Settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB por defecto
ALLOWED_MIME_TYPES: List[str] = [
    "video/mp4",
    "video/mov",
    "video/avi",
    "video/mkv",
]

# Modelo Whisper dummy (parcheable en tests)
class DummyWhisper:
    def transcribe(self, path: str, language: str = "es"):
        return {"text": ""}

whisper_model = DummyWhisper()

# Función de análisis dummy (se parchea en tests)
def analizar_con_mistral(transcripcion: str) -> str:
    return ""

app = FastAPI()

@app.post("/analizar/")
async def analizar(file: UploadFile = File(...)):
    # Validar MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido.")

    data = await file.read()

    # Validar tamaño
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Archivo demasiado grande.")

    file_path = MEDIA_ROOT / file.filename
    with open(file_path, "wb") as f:
        f.write(data)

    try:
        resultado = whisper_model.transcribe(str(file_path), language="es")
        transcripcion = resultado.get("text", "")
        recomendaciones = analizar_con_mistral(transcripcion)
    except Exception:
        raise HTTPException(status_code=500, detail="Error en el procesamiento de IA.")
    finally:
        if file_path.exists():
            file_path.unlink()

    return JSONResponse(
        content={"transcripcion": transcripcion, "recomendaciones": recomendaciones}
    )
