#!/bin/bash

# Script de instalación rápida para ViralBoostAI MVP
# Autor: ViralBoostAI Team

set -e

echo "🚀 ViralBoostAI MVP - Instalación Rápida"
echo "=========================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "💡 Instala Python 3.8+ desde https://python.org"
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Instalación completada!"
echo ""
echo "🎯 Para ejecutar el servidor:"
echo "   python3 start_server.py"
echo ""
echo "🌐 O manualmente:"
echo "   source venv/bin/activate"
echo "   python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "📱 Abre http://localhost:8000/static/index.html en tu navegador" 