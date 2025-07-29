from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import base64
import os
from pathlib import Path

app = FastAPI(title="ViralBoostAI Demo Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
frontend_static_dir = Path(__file__).resolve().parent.parent / "frontend" / "static"
if frontend_static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_static_dir)), name="static")

class AnalyzeRequest(BaseModel):
    filename: str
    content: str  # base64 encoded string

@app.post("/api/analizar")
async def analyze(payload: AnalyzeRequest):
    try:
        decoded = base64.b64decode(payload.content)
        filepath = f"/tmp/{payload.filename}"
        with open(filepath, "wb") as f:
            f.write(decoded)
        
        # Simulamos respuesta de IA
        return {
            "transcripcion": "Transcripción de ejemplo. (La transcripción completa no está disponible en el modo demo.)",
            "recomendaciones": {
                "hashtags": ["#TikTok", "#Viral", "#ParaTi", "#Trendy", "#España"],
                "resumen": "Resumen: Este video trata sobre un ejemplo de contenido para TikTok. Se recomienda usar hashtags relevantes y mantener un tono cercano con la audiencia.",
                "recomendaciones": [
                    "Incluye un hook interesante en los primeros 3 segundos",
                    "Usa subtítulos para mayor accesibilidad",
                    "Mantén el ritmo dinámico durante todo el video"
                ]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {"mensaje": "¡Backend demo de ViralBoostAI funcionando!"}

@app.get("/")
async def root():
    return {"mensaje": "ViralBoostAI backend running"} 