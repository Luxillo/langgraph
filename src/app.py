# src/app.py
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ✅ 1) Cargar .env desde la raíz del repo (aunque ejecutes desde otro lado)
REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
import logging
logging.basicConfig(
    level=logging.INFO,  # cambia a DEBUG si quieres más detalle
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("langgraph-demo")

# ✅ 2) Importar graph DESPUÉS de cargar env
from src.graph import build_graph


app = FastAPI(title="Pragma LangGraph Multiagent Template")

# Compilamos el grafo una vez al iniciar (rápido y estable)
graph = build_graph(save_diagram=True)

# Montamos carpeta estática (para imágenes generadas)
repo_root = Path(__file__).resolve().parents[1]  # src/app.py -> repo_root
static_dir = repo_root / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(body: ChatIn):
    """
    Flujo:
    1) Entramos con el mensaje del usuario.
    2) Invocamos el grafo.
    3) Devolvemos el último mensaje como respuesta final.
    """
    state = {"messages": [HumanMessage(content=body.message)]}
    out = graph.invoke(state)

    final_msg = out["messages"][-1]
    answer = getattr(final_msg, "content", str(final_msg))

    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))

    uvicorn.run("src.app:app", host=host, port=port, reload=True)
