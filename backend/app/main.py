# backend/app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Cargar variables de entorno desde backend/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

app = FastAPI(
    title="ViralBoostAI Backend",
    description="API para transcripción y análisis de videos",
    version="0.1.0"
)

# Configurar CORS (ajusta allow_origins en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Montar carpeta de archivos estáticos (frontend)
proyecto_root = os.path.dirname(__file__)  # apunta a backend/app
carpeta_frontend = os.path.abspath(os.path.join(proyecto_root, "../..", "frontend/static"))
app.mount("/static", StaticFiles(directory=carpeta_frontend), name="static")

# Importar y registrar el router de api/endpoints.py
from .api.endpoints import router as api_router
app.include_router(api_router)


@app.get("/")
async def root():
    """
    Punto de entrada principal; confirma que el backend está corriendo.
    El frontend se debe acceder en /static/index.html
    """
    return {"mensaje": "¡Backend de ViralBoostAI funcionando!"}






