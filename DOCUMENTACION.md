# 🎯 Documentación - Índice

## 📚 Documentación de Herramientas Analíticas

**Ubicación**: [`docs/`](docs/)

### Documentos Principales

| Documento | Descripción | Duración |
|-----------|-------------|----------|
| [docs/README.md](docs/README.md) | 📖 Índice general | 5 min |
| [docs/QUICK_START_ANALYTICS.md](docs/QUICK_START_ANALYTICS.md) | 🚀 Inicio rápido | 5 min |
| [docs/ANALYTICS_TOOLS.md](docs/ANALYTICS_TOOLS.md) | 📊 Documentación completa | 15 min |
| [docs/IMPLEMENTACION_HERRAMIENTAS.md](docs/IMPLEMENTACION_HERRAMIENTAS.md) | 🔧 Resumen técnico | 10 min |

---

## 🚀 Inicio Rápido

```bash
# 1. Leer guía rápida
cat docs/QUICK_START_ANALYTICS.md

# 2. Ejecutar pruebas
python3 scripts/test_analytics.py

# 3. Iniciar servidor
python -m uvicorn src.app:app --port 8000 --reload

# 4. Probar consultas
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuánto vendimos?"}'
```

---

## 📖 Selecciona tu Ruta

### 👶 Soy nuevo en el proyecto
→ [docs/QUICK_START_ANALYTICS.md](docs/QUICK_START_ANALYTICS.md)

### 👨‍💻 Soy desarrollador
→ [docs/ANALYTICS_TOOLS.md](docs/ANALYTICS_TOOLS.md)

### 🔍 Quiero entender la arquitectura
→ [docs/IMPLEMENTACION_HERRAMIENTAS.md](docs/IMPLEMENTACION_HERRAMIENTAS.md)

### 📚 Quiero ver todo
→ [docs/README.md](docs/README.md)

---

**Toda la documentación está en el directorio [`docs/`](docs/)**
