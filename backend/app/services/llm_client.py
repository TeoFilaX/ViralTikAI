# backend/app/services/llm_client.py

import os
import json
import ctypes
from typing import Optional

from fastapi import HTTPException

try:
    import openai
except ImportError:
    openai = None

# Cargar variables de entorno (asegúrate de haberlas cargado en main.py)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_MODEL_PATH = os.getenv("MISTRAL_MODEL_PATH", "")

def generar_analisis_llm(prompt: str, modelo: str = "openai", max_tokens: int = 1024) -> dict:
    """
    Invoca al LLM seleccionado con el prompt dado:
      - Si modelo="openai", usa la API de OpenAI (GPT-4).
      - Si modelo="mistral", usa ctransformers para llamar al modelo local.
    Retorna un diccionario con la respuesta parseada (si es JSON) o el texto crudo.
    """
    if modelo == "openai":
        return _llm_openai(prompt, max_tokens)
    elif modelo == "mistral":
        return _llm_mistral_local(prompt, max_tokens)
    else:
        raise HTTPException(status_code=400, detail=f"Modelo LLM desconocido: {modelo}")

def _llm_openai(prompt: str, max_tokens: int) -> dict:
    """
    Llamada básica a OpenAI ChatCompletion (GPT-4).
    Devuelve la respuesta como JSON (si el modelo retorna texto con formato JSON) o como texto plano en {"text": ...}.
    """
    if openai is None or OPENAI_API_KEY is None:
        raise HTTPException(status_code=500, detail="OpenAI no está configurado correctamente.")
    openai.api_key = OPENAI_API_KEY
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        contenido = respuesta.choices[0].message.content.strip()
        # Intentar parsear JSON si el modelo devuelve un objeto estructurado
        try:
            return json.loads(contenido)
        except json.JSONDecodeError:
            return {"text": contenido}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en llamada a OpenAI: {e}")

def _llm_mistral_local(prompt: str, max_tokens: int) -> dict:
    """
    Llamada básica a modelo local Mistral vía ctransformers (gguf).
    Retorna la respuesta como texto en {"text": ...}.
    """
    if not MISTRAL_MODEL_PATH:
        raise HTTPException(status_code=500, detail="Ruta al modelo Mistral no definida.")
    try:
        # Ejemplo con ctransformers:
        from ctransformers import AutoModelForCausalLM, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(MISTRAL_MODEL_PATH)
        model = AutoModelForCausalLM.from_pretrained(
            MISTRAL_MODEL_PATH, model_type="mistral", 
            dtype="float16",  # Q4_K_M usa int4 o int8; ajustar según convenga
            use_gpu=False
        )
        entradas = tokenizer.encode(prompt)
        salidas = model.generate(entradas, max_new_tokens=max_tokens)
        texto = tokenizer.decode(salidas, skip_special_tokens=True)
        return {"text": texto}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en llamada a Mistral local: {e}")
