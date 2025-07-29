# 🤝 Contribuir a ViralBoostAI MVP

¡Gracias por tu interés en contribuir a ViralBoostAI! Este documento te guiará a través del proceso de contribución.

## 🎯 ¿Cómo puedo contribuir?

### 🐛 Reportar Bugs
- Usa el template de issue para bugs
- Incluye pasos para reproducir el problema
- Adjunta logs y capturas de pantalla si es relevante

### 💡 Sugerir Mejoras
- Usa el template de issue para features
- Describe la funcionalidad que te gustaría ver
- Explica por qué sería útil

### 🔧 Contribuir Código
1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz tus cambios
4. Ejecuta los tests
5. Envía un Pull Request

## 🛠️ Configuración del Entorno de Desarrollo

### Prerrequisitos
- Python 3.8+
- Git
- Navegador web moderno

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/TeoFilaX/ViralBoostAI.git
cd ViralBoostAI

# Instalar dependencias
./install.sh

# Ejecutar el servidor
python3 start_server.py
```

## 🧪 Testing

### Tests Automáticos
```bash
python3 run_manual_tests.py
```

### Tests Manuales
```bash
# Probar el endpoint de salud
curl http://localhost:8000/api/health

# Probar análisis
curl -X POST http://localhost:8000/api/analizar \
  -H "Content-Type: application/json" \
  -d '{"filename":"test.mp4","content":"dGVzdA=="}'
```

## 📝 Estándares de Código

### Python
- Usa PEP 8 para estilo de código
- Incluye docstrings en funciones
- Escribe tests para nuevas funcionalidades

### JavaScript/HTML
- Usa indentación consistente
- Comenta código complejo
- Valida HTML/CSS

### Commits
- Usa mensajes descriptivos
- Incluye emojis para categorizar
- Ejemplo: `🚀 Add new video analysis feature`

## 🔄 Proceso de Pull Request

1. **Fork** el repositorio
2. **Crea** una rama: `git checkout -b feature/nueva-funcionalidad`
3. **Haz** tus cambios
4. **Commitea**: `git commit -m "🚀 Add nueva funcionalidad"`
5. **Push**: `git push origin feature/nueva-funcionalidad`
6. **Abre** un Pull Request

## 📋 Checklist para Pull Requests

- [ ] El código sigue los estándares del proyecto
- [ ] Se han agregado tests para nuevas funcionalidades
- [ ] Los tests pasan correctamente
- [ ] La documentación ha sido actualizada
- [ ] El commit message es descriptivo

## 🏷️ Etiquetas de Issues

- `🐛 bug` - Reporte de bug
- `💡 enhancement` - Mejora sugerida
- `🚀 feature` - Nueva funcionalidad
- `📚 documentation` - Mejoras en documentación
- `🧪 test` - Tests
- `🔧 refactor` - Refactorización de código

## 📞 Contacto

Si tienes preguntas sobre cómo contribuir:
- Abre un issue en GitHub
- Contacta al equipo de desarrollo
- Revisa la documentación existente

---

**¡Gracias por contribuir a ViralBoostAI! 🚀** 