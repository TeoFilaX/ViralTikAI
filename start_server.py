#!/usr/bin/env python3
"""
Script de inicio para ViralBoostAI MVP
Ejecuta el servidor FastAPI con configuración optimizada
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} - OK")

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencias instaladas - OK")
    except ImportError as e:
        print(f"❌ Error: Falta instalar dependencias: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        sys.exit(1)

def start_server():
    """Inicia el servidor FastAPI"""
    print("🚀 Iniciando ViralBoostAI MVP...")
    print("📁 Directorio actual:", os.getcwd())
    
    # Comando para ejecutar el servidor
    cmd = [
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    print("🌐 Servidor iniciándose en: http://localhost:8000")
    print("📱 Frontend disponible en: http://localhost:8000/static/index.html")
    print("🔧 API docs en: http://localhost:8000/docs")
    print("\n⏹️  Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido. ¡Hasta luego!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🎯 ViralBoostAI MVP - Script de Inicio")
    print("=" * 40)
    
    check_python_version()
    check_dependencies()
    start_server() 