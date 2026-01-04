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
from fastapi import Depends
from src.api import db_tools


app = FastAPI(title="Pragma LangGraph Multiagent Template")

# Compilamos el grafo una vez al iniciar (rápido y estable)
graph = build_graph(save_diagram=True)

# Montamos carpeta estática (para imágenes generadas)
repo_root = Path(__file__).resolve().parents[1]  # src/app.py -> repo_root
static_dir = repo_root / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include DB tools router for manual testing
app.include_router(db_tools.router)


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(body: ChatIn):
    """
    Flujo:
    1) Entramos con el mensaje del usuario.
    2) Invocamos el grafo.
    3) Extraemos datos de ToolMessage o respuesta del LLM.
    """
    from langchain_core.messages import ToolMessage
    import json
    
    state = {"messages": [HumanMessage(content=body.message)]}
    
    try:
        out = graph.invoke(state, config={"recursion_limit": 10})
    except Exception as e:
        logger.error(f"Error en grafo: {e}")
        return {"answer": f"Error: {str(e)[:100]}"}

    # Buscar ToolMessage o respuesta final
    tool_data = None
    
    for msg in out["messages"]:
        if isinstance(msg, ToolMessage):
            # Extraer datos de la herramienta
            try:
                content = msg.content
                # Si es string JSON, parsearlo
                if isinstance(content, str):
                    tool_data = json.loads(content)
                else:
                    tool_data = content
                    
                if tool_data:
                    logger.info(f"✅ Datos retornados: {len(tool_data) if isinstance(tool_data, list) else 1} registros")
                    # Formatear como tabla
                    if isinstance(tool_data, list) and tool_data:
                        formatted = "📊 **Resultados:**\n\n"
                        formatted += "```json\n"
                        formatted += json.dumps(tool_data, ensure_ascii=False, indent=2)
                        formatted += "\n```"
                        return {"answer": formatted}
            except:
                pass

    # Si no hay ToolMessage, retornar respuesta del LLM
    final_msg = out["messages"][-1]
    answer = getattr(final_msg, "content", str(final_msg))

    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))

    uvicorn.run("src.app:app", host=host, port=port, reload=True)
