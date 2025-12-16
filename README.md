# 🤖 Bot Multiagente – LangGraph (Demo)

Este repositorio contiene una **demo simple de un bot multiagente** construido con **LangGraph**, cuyo objetivo es mostrar cómo:

* Un agente decide cuándo usar herramientas
* Se integran **múltiples proveedores de IA** (Azure OpenAI y OpenAI directo)
* Se pueden generar **artefactos** (ej. imágenes) y exponerlos vía API
* El diseño es **replicable** para otros clientes o casos de uso

> ⚠️ Este bot es deliberadamente **minimalista**.
> El foco está en la **arquitectura y el flujo multiagente**, no en la UI ni en features avanzadas.

---

## 🧠 ¿Qué hace este bot?

El bot puede:

* 💬 Responder de forma conversacional
* 🌤️ Consultar el **clima actual** de una ciudad (tool externa)
* 🖼️ **Generar imágenes** a partir de texto (tool especializada)
* 🔀 Decidir automáticamente **qué herramienta usar** según la intención del usuario

Todo esto es orquestado por **LangGraph**, siguiendo el patrón:

```
Usuario → Agente → Tool (si aplica) → Agente → Respuesta final
```

---

## 🏗️ Arquitectura (alto nivel)

* **LangGraph**: orquestación del flujo agent ↔ tools
* **Azure OpenAI (GPT-4o)**:

  * Razonamiento
  * Conversación
  * Decisión de herramientas
* **OpenAI directo (GPT-4o)**:

  * Generación de imágenes
* **FastAPI**:

  * Exposición del endpoint `/chat`
  * Servir archivos estáticos (`/static`)
* **Streamlit**:

  * Interfaz de chat simple para demo

---

## 📂 Estructura del proyecto

```
.
├── src/
│   ├── app.py              # API FastAPI
│   ├── graph.py            # Grafo LangGraph
│   ├── prompts/
│   │   └── system.md       # Prompt principal del agente
│   ├── tools/
│   │   ├── weather.py      # Tool: clima (Open-Meteo)
│   │   └── image.py        # Tool: generación de imágenes (OpenAI)
│   └── llm.py              # Cliente LLM (Azure OpenAI)
├── static/
│   └── generated/          # Imágenes generadas
├── streamlit_app.py        # UI Streamlit
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Variables de entorno

Crea un archivo `.env` a partir de `.env.example`.

### Azure OpenAI (chat y razonamiento)

```env
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
```

### OpenAI directo (solo imágenes)

```env
OPENAI_API_KEY=sk-...
OPENAI_IMAGE_MODEL=gpt-4o
```

### Exposición pública de archivos

```env
PUBLIC_BASE_URL=http://localhost:8000
```

---

## ▶️ Cómo ejecutar el bot

### 1️⃣ Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Levantar la API

```bash
python -m uvicorn src.app:app --reload --port 8000
```

La API quedará disponible en:

```
http://localhost:8000/chat
```

---

### 3️⃣ Levantar la interfaz Streamlit

En otra terminal:

```bash
streamlit run streamlit_app.py
```

---

## 🔁 Contrato de la API

### Request

```json
POST /chat
{
  "message": "Genera un mapa minimalista de Colombia"
}
```

### Response

```json
{
  "answer": "Markdown con texto e imágenes"
}
```

Las imágenes se devuelven como **URLs absolutas** servidas desde `/static`.

---

## 🧪 Ejemplos de uso

* **Clima**

  > “¿Cómo está el clima en Roma hoy?”

* **Imagen**

  > “Genera un mapa minimalista de Colombia en estilo flat”

---

## 🎯 Propósito del repositorio

Este proyecto sirve como:

* 📚 Ejemplo didáctico para charlas técnicas
* 🧩 Plantilla base para nuevos agentes
* 🔁 Artefacto replicable para otros clientes
* 🧠 Referencia de uso real de LangGraph en producción

No pretende ser un producto final ni una solución completa.

---

## 📌 Notas finales

* El comportamiento del agente está gobernado por:

  * `system.md` (prompt)
  * tools registradas con `@tool`
* Agregar una nueva tool implica:

  1. Crear el archivo en `src/tools`
  2. Decorar la función
  3. Importarla en `graph.py`

---

## 👩‍💻 Autoria

Desarrollado como demo técnica para charlas internas sobre **multiagentes y LangGraph**.

