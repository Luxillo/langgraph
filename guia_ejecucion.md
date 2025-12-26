# 🚀 Guía de Ejecución - Bot Multiagente LangGraph

Esta guía te llevará paso a paso para ejecutar el bot multiagente con Qwen3:8B local.

---

## 📋 Prerrequisitos

- **Python 3.8+**
- **Ollama** instalado y corriendo
- **Git** (para clonar el repositorio)

---

## 🛠️ Instalación de Ollama

### macOS/Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows:
Descargar desde: https://ollama.ai/download

### Verificar instalación:
```bash
ollama --version
```

---

## 🚀 Pasos para ejecutar

### **1️⃣ Preparar el entorno**

```bash
# Navegar al directorio del proyecto
cd langgraph

# Crear entorno virtual
# mv .venv .venv-old
# python -m venv .venv
python3.13 -m venv .venv


# Activar entorno virtual
source .venv/bin/activate  # macOS/Linux
# o
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### **2️⃣ Configurar variables de entorno**

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# El archivo .env ya está configurado para usar Qwen3:8B local
# No necesitas modificar nada si usas la configuración por defecto
```

### **3️⃣ Verificar Ollama y modelo**

```bash
# Iniciar Ollama (si no está corriendo)
ollama serve

# En otra terminal, verificar modelos disponibles
ollama list

brew services start ollama

brew services stop ollama

# Si no tienes qwen3:8b, descargarlo (puede tardar varios minutos)
ollama pull qwen3:8b

# Verificar que la API de Ollama responde
curl http://localhost:11434/api/tags
```

### **4️⃣ Ejecutar la API FastAPI (Terminal 1)**

```bash
# Desde la carpeta del proyecto (con .venv activado)
python -m uvicorn src.app:app --reload --port 8000
```

**✅ Deberías ver:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**🌐 API disponible en:** http://localhost:8000

### **5️⃣ Ejecutar interfaz Streamlit (Terminal 2)**

```bash
# En otra terminal, misma carpeta (con .venv activado)
streamlit run streamlit_app.py
```

**✅ Se abrirá automáticamente en:** http://localhost:8501

---

## 🧪 Pruebas sugeridas

Una vez que ambos servicios estén corriendo, prueba estos ejemplos:

1. **💬 Chat básico:**
   > "Hola, ¿cómo estás?"

2. **🌤️ Consulta del clima:**
   > "¿Cómo está el clima en Madrid hoy?"

3. **🖼️ Generación de imágenes:**
   > "Genera una imagen de un gato minimalista"

---

## 🔧 Solución de problemas

### **Ollama no responde:**
```bash
# Verificar si Ollama está corriendo
ps aux | grep ollama

# Si no está corriendo, iniciarlo
ollama serve

# Verificar conectividad
curl http://localhost:11434/api/tags
```

### **Error de dependencias:**
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### **Puerto ocupado:**
```bash
# Para la API (cambiar puerto)
python -m uvicorn src.app:app --reload --port 8001

# Actualizar en streamlit_app.py la línea:
# API_URL = "http://localhost:8001/chat"
```

### **Modelo no encontrado:**
```bash
# Verificar modelos disponibles
ollama list

# Descargar modelo si no existe
ollama pull qwen3:8b

# Verificar que el nombre coincida en .env
# OLLAMA_MODEL=qwen3:8b
```

### **Error de conexión en Streamlit:**
- Verificar que la API esté corriendo en http://localhost:8000
- Revisar el indicador de estado en el sidebar de Streamlit
- Verificar logs en la terminal de la API

---

## 📁 Estructura de archivos

```
langgraph/
├── src/
│   ├── app.py              # API FastAPI
│   ├── graph.py            # Grafo LangGraph
│   ├── llm.py              # Cliente LLM
│   ├── prompts/
│   │   └── system.md       # Prompt del sistema
│   └── tools/
│       ├── weather.py      # Tool: clima
│       └── image.py        # Tool: imágenes
├── static/generated/       # Imágenes generadas
├── streamlit_app.py        # Interfaz Streamlit
├── .env                    # Variables de entorno
├── .env.example           # Ejemplo de configuración
├── requirements.txt       # Dependencias
└── guia_ejecucion.md     # Esta guía
```

---

## 🎯 URLs importantes

- **API FastAPI:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs
- **Interfaz Streamlit:** http://localhost:8501
- **Ollama API:** http://localhost:11434

---

## 🛑 Detener los servicios

```bash
# En cada terminal, presionar:
Ctrl + C

# Desactivar entorno virtual
deactivate
```

---

¡Listo! 🎉 Tu bot multiagente debería estar funcionando correctamente.