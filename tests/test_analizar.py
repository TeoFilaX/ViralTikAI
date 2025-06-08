# Archivo: tests/test_analizar.py

import io
import os
import pytest
from fastapi.testclient import TestClient
from pathlib import Path

# Importa la app y las constantes desde backend/main.py
from backend.main import (
    app,
    MEDIA_ROOT,
    MAX_FILE_SIZE,
    ALLOWED_MIME_TYPES,
    whisper_model,
    analizar_con_mistral,
)

# Creamos un cliente de prueba
client = TestClient(app)

# Fixture para parchear whisper_model.transcribe y analizar_con_mistral
@pytest.fixture(autouse=True)
def patch_models(monkeypatch):
    # Parcheamos whisper_model.transcribe para que devuelva un dict con texto fijo
    def fake_transcribe(path, language):
        return {"text": "esta es una transcripción de prueba"}
    monkeypatch.setattr(whisper_model, "transcribe", fake_transcribe)

    # Parcheamos analizar_con_mistral para que devuelva siempre un string fijo
    def fake_mistral(transcripcion):
        return "hashtags: #test\nhora: 12:00\n"
    monkeypatch.setattr("backend.main.analizar_con_mistral", fake_mistral)

    yield

    # Cleanup: borrar MEDIA_ROOT tras cada test
    for f in MEDIA_ROOT.iterdir():
        try:
            f.unlink()
        except:
            pass

def create_dummy_video_bytes(size_bytes: int) -> bytes:
    """
    Genera un contenido binario 'simulando' un video, de la longitud solicitada.
    No es un MP4 real, pero basta para los tests de tamaño y mime-type.
    """
    return b"\x00" * size_bytes

def test_analizar_video_valido(tmp_path, monkeypatch):
    """
    Enviamos un archivo con mime-type permitido y tamaño bajo MAX_FILE_SIZE.
    Debe devolver 200 y campos 'transcripcion' y 'recomendaciones'.
    """
    file_content = create_dummy_video_bytes(1024)  # 1 KB
    file_name = "video_de_prueba.mp4"
    files = {
        "file": (
            file_name,
            io.BytesIO(file_content),
            "video/mp4"
        )
    }

    response = client.post("/analizar/", files=files)
    assert response.status_code == 200

    data = response.json()
    assert "transcripcion" in data
    assert data["transcripcion"] == "esta es una transcripción de prueba"
    assert "recomendaciones" in data
    assert data["recomendaciones"].startswith("hashtags: #test")

    # Comprobamos que el archivo original se eliminó de MEDIA_ROOT
    saved_path = MEDIA_ROOT / file_name
    assert not saved_path.exists()

def test_mime_type_no_permitido():
    """
    Enviamos un archivo con mime-type no permitido (por ejemplo, image/png).
    Debe devolver 400.
    """
    file_content = create_dummy_video_bytes(512)
    files = {
        "file": (
            "imagen.png",
            io.BytesIO(file_content),
            "image/png"
        )
    }

    response = client.post("/analizar/", files=files)
    assert response.status_code == 400
    assert response.json()["detail"] == "Tipo de archivo no permitido."

def test_archivo_demasiado_grande(monkeypatch):
    """
    Forzamos que MAX_FILE_SIZE sea pequeño (por ejemplo, 10 bytes) y
    enviamos un 'video' de 100 bytes. Debe devolver 413.
    """
    # Parcheamos temporalmente MAX_FILE_SIZE a 10 bytes
    monkeypatch.setattr("backend.main.MAX_FILE_SIZE", 10)

    file_content = create_dummy_video_bytes(100)
    files = {
        "file": (
            "video_grande.mp4",
            io.BytesIO(file_content),
            "video/mp4"
        )
    }

    response = client.post("/analizar/", files=files)
    assert response.status_code == 413
    assert response.json()["detail"] == "Archivo demasiado grande."

    # Asegurarnos de que no quedó ningún archivo en MEDIA_ROOT
    saved_path = MEDIA_ROOT / "video_grande.mp4"
    assert not saved_path.exists()

def test_error_interno_en_procesamiento(monkeypatch):
    """
    Simulamos que whisper_model.transcribe lanza una excepción. Debe devolver 500.
    """
    # Parcheamos transcribe para que levante excepción
    def raise_error(path, language):
        raise RuntimeError("Fallo en Whisper")
    monkeypatch.setattr(whisper_model, "transcribe", raise_error)

    file_content = create_dummy_video_bytes(1024)
    files = {
        "file": (
            "video_error.mp4",
            io.BytesIO(file_content),
            "video/mp4"
        )
    }

    response = client.post("/analizar/", files=files)
    assert response.status_code == 500
    assert response.json()["detail"] == "Error en el procesamiento de IA."

    # Verificar que el archivo fue eliminado
    saved_path = MEDIA_ROOT / "video_error.mp4"
    assert not saved_path.exists()
