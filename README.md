# ViralBoostAI

## Descripción

ViralBoostAI es una plataforma para optimizar vídeos con inteligencia artificial. Permite subir un vídeo para análisis y genera recomendaciones como transcripción, hashtags, y métricas predictivas. Incluye un asistente de chat para sugerencias en tiempo real.

## Estructura de Carpetas

```
ViralBoostAI/
├── backend/
│   ├── main.py
│   └── requirements.txt
└── static/
    ├── index.html
    ├── privacy.html
    └── style.css
```

## Instrucciones de Uso

1. Navegar al directorio `backend`:
   ```bash
   cd backend
   ```

2. Crear un entorno virtual e instalar dependencias:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Ejecutar el servidor:
   ```bash
   uvicorn main:app --reload
   ```

4. Abrir `http://127.0.0.1:8000` en el navegador para acceder a la aplicación.

## Nota

El endpoint `/analizar/` devuelve datos simulados para demostración. Ajustar según la lógica real de backend.
