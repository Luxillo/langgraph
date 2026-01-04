# src/graph.py
"""
LangGraph - Plantilla Multiagente (patrón 'agent tool-use')..

Qué hace este archivo:
1) Define un State con merge correcto (messages se acumula).
2) Crea un grafo LangGraph con:
   - Nodo 'agent': llama al LLM (Azure OpenAI) con tools bindeadas
   - Nodo 'tools': ejecuta tools (ToolNode)
   - Loop agent <-> tools hasta que no haya más tool_calls
3) Compila el grafo y guarda un diagrama Mermaid en /artifacts/graph.mmd
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TypedDict, List, Annotated
from uuid import uuid4

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from src.llm import get_llm

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages  # ✅ merge correcto del historial

from src.tools.weather import get_weather
from src.tools.image import generate_image
from src.tools.database.product_tools import search_products_by_name, get_low_stock_products
from src.tools.database.analytics_tools import (
    sales_by_date,
    sales_by_employee,
    sales_by_payment_method,
    average_transaction_value,
    top_employees_by_sales,
    top_products_by_quantity,
    revenue_by_product_category,
    low_stock_products,
    inventory_rotation,
    total_inventory_value,
    inventory_by_category,
    most_frequent_customers,
    average_customer_ticket,
    preferred_payment_methods,
    revenue_by_supplier,
    sales_vs_inventory_by_category,
)
import logging
logger = logging.getLogger("langgraph-demo.graph")

# ============================================================================
# UTILITY: Intelligent Intent Matching
# ============================================================================

def _detect_tool_from_intent(query: str) -> dict | None:
    """
    Detecta automáticamente qué herramienta usar basado en la intención del usuario.
    Retorna dict con tool_name y parameters, o None si no detecta intent.
    """
    if not query:
        return None
    
    query_lower = query.lower()
    
    # Keywords para cada herramienta
    # PRODUCTOS
    if any(word in query_lower for word in ["top", "productos más vendidos", "qué se vende", "best selling", "más vendido"]):
        top_n = _extract_number(query_lower, default=10)
        fecha_inicio, fecha_fin = _extract_dates(query_lower)
        return {
            'tool_name': 'top_products_by_quantity',
            'parameters': {'top_n': top_n, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        }
    
    # VENTAS POR FECHA
    if any(word in query_lower for word in ["cuánto vendimos", "ventas por fecha", "ventas en", "ingresos en", "revenue by date"]):
        fecha_inicio, fecha_fin = _extract_dates(query_lower)
        return {
            'tool_name': 'sales_by_date',
            'parameters': {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        }
    
    # MEJORES VENDEDORES
    if any(word in query_lower for word in ["mejor vendedor", "top empleado", "best salesperson", "quién vendió", "empleado más"]):
        top_n = _extract_number(query_lower, default=5)
        fecha_inicio, fecha_fin = _extract_dates(query_lower)
        return {
            'tool_name': 'top_employees_by_sales',
            'parameters': {'top_n': top_n, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        }
    
    # STOCK BAJO
    if any(word in query_lower for word in ["stock bajo", "qué falta", "low stock", "inventario bajo", "productos sin"]):
        return {
            'tool_name': 'get_low_stock_products',
            'parameters': {'threshold': 100}
        }
    
    # ROTACIÓN DE INVENTARIO
    if any(word in query_lower for word in ["rotación", "gira rápido", "baja rotación", "inventory rotation", "fast moving"]):
        fecha_inicio, fecha_fin = _extract_dates(query_lower)
        return {
            'tool_name': 'inventory_rotation',
            'parameters': {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        }
    
    # VALOR TOTAL INVENTARIO
    if any(word in query_lower for word in ["cuánto vale", "valor del stock", "inventory value", "total inventario"]):
        return {
            'tool_name': 'total_inventory_value',
            'parameters': {}
        }
    
    # INVENTARIO POR CATEGORÍA
    if any(word in query_lower for word in ["inventario por categoría", "stock por tipo", "inventory by category"]):
        return {
            'tool_name': 'inventory_by_category',
            'parameters': {}
        }
    
    # CLIENTES FRECUENTES
    if any(word in query_lower for word in ["mejores clientes", "cliente frecuente", "quién compra", "best customers", "top client"]):
        top_n = _extract_number(query_lower, default=10)
        fecha_inicio, fecha_fin = _extract_dates(query_lower)
        return {
            'tool_name': 'most_frequent_customers',
            'parameters': {'top_n': top_n, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        }
    
    # INGRESOS POR CATEGORÍA
    if any(word in query_lower for word in ["ingresos por categoría", "revenue by category", "ventas por tipo", "qué categoría genera"]):
        fecha_inicio, fecha_fin = _extract_dates(query_lower)
        return {
            'tool_name': 'revenue_by_product_category',
            'parameters': {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        }
    
    # MÉTODOS DE PAGO
    if any(word in query_lower for word in ["método de pago", "payment method", "efectivo", "tarjeta", "cómo pagan"]):
        fecha_inicio, fecha_fin = _extract_dates(query_lower)
        return {
            'tool_name': 'preferred_payment_methods',
            'parameters': {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        }
    
    # INGRESOS POR PROVEEDOR
    if any(word in query_lower for word in ["proveedor", "supplier", "ingresos de", "revenue by supplier"]):
        fecha_inicio, fecha_fin = _extract_dates(query_lower)
        return {
            'tool_name': 'revenue_by_supplier',
            'parameters': {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        }
    
    # DEMANDA VS STOCK
    if any(word in query_lower for word in ["demanda vs stock", "reabastecimiento", "demand vs inventory", "qué necesita stock"]):
        fecha_inicio, fecha_fin = _extract_dates(query_lower)
        return {
            'tool_name': 'sales_vs_inventory_by_category',
            'parameters': {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        }
    
    return None


def _extract_number(text: str, default: int = 10) -> int:
    """Extrae un número de un texto. Ej: 'top 5' -> 5"""
    import re
    matches = re.findall(r'\d+', text)
    if matches:
        return int(matches[0])
    return default


def _extract_dates(text: str) -> tuple[str, str]:
    """
    Extrae rango de fechas del texto.
    Maneja: 'enero', 'este mes', 'última semana', 'marzo', etc.
    Retorna: (fecha_inicio, fecha_fin) en formato 'YYYY-MM-DD'
    """
    from datetime import datetime, timedelta
    
    today = datetime(2025, 1, 3)  # Fecha del sistema
    
    months = {
        'enero': (1, 1), 'febrero': (2, 1), 'marzo': (3, 1), 'abril': (4, 1),
        'mayo': (5, 1), 'junio': (6, 1), 'julio': (7, 1), 'agosto': (8, 1),
        'septiembre': (9, 1), 'octubre': (10, 1), 'noviembre': (11, 1), 'diciembre': (12, 1),
    }
    
    text_lower = text.lower()
    
    # Detectar mes específico
    for month_name, (month, _) in months.items():
        if month_name in text_lower:
            start = datetime(2025, month, 1)
            # Calcular último día del mes
            if month == 12:
                end = datetime(2025, 12, 31)
            else:
                end = datetime(2025, month + 1, 1) - timedelta(days=1)
            return (start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    
    # "Este mes"
    if 'este mes' in text_lower:
        start = datetime(2025, today.month, 1)
        if today.month == 12:
            end = datetime(2025, 12, 31)
        else:
            end = datetime(2025, today.month + 1, 1) - timedelta(days=1)
        return (start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    
    # "Última semana"
    if 'última semana' in text_lower or 'last week' in text_lower:
        end = today
        start = today - timedelta(days=7)
        return (start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    
    # Default: todo el año
    return ('2025-01-01', '2025-12-31')



# -----------------------------
# 1) Estado compartido del grafo
# -----------------------------
class AgentState(TypedDict):
    """
    messages: historial del chat.
    add_messages garantiza que cada nodo "agrega" mensajes en vez de reemplazarlos.
    """
    messages: Annotated[List[BaseMessage], add_messages]


# -----------------------------
# 2) Prompt de sistema (editable)
# -----------------------------
def _load_system_prompt() -> str:
    """
    Carga el prompt desde /src/prompts/system.md.
    Si no existe, usa un prompt por defecto (para que el repo siempre arranque).
    """
    p = Path(__file__).parent / "prompts" / "system.md"
    if p.exists():
        return p.read_text(encoding="utf-8")

    return (
        "Eres un asistente técnico. Responde en español, claro y breve.\n\n"
        "Si la pregunta requiere datos externos, usa una herramienta.\n"
        "Herramientas disponibles:\n"
        "- get_weather(location): clima actual por ciudad\n"
        "- generate_image(prompt): genera imagen y retorna ruta\n\n"
        "search_products_by_name(name): busca productos en la base de datos por nombre\n"
        "get_low_stock_products(threshold): lista productos con stock bajo\n\n"
        "Si el usuario pregunta por clima, extrae la ciudad del mensaje y llama get_weather.\n"
        "Si el usuario pide una imagen, llama generate_image con un prompt corto.\n"
        "Después de usar herramientas, redacta la respuesta final."
    )


# -----------------------------
# 3) LLM Azure OpenAI - Agente principal
# -----------------------------
def _get_llm() -> BaseChatModel:
    """
    LLM único. Usa el cliente centralizado (Ollama por defecto).
    """
    return get_llm()


# -----------------------------
# 4) Construcción del grafo
# -----------------------------
def build_graph(save_diagram: bool = True):
    """
    Construye y compila el grafo. Con save_diagram=True guarda Mermaid.
    """

    # Tools registradas con @tool
    tools = [
        get_weather,
        generate_image,
        search_products_by_name,
        get_low_stock_products,
        # Analytics tools
        sales_by_date,
        sales_by_employee,
        sales_by_payment_method,
        average_transaction_value,
        top_employees_by_sales,
        top_products_by_quantity,
        revenue_by_product_category,
        low_stock_products,
        inventory_rotation,
        total_inventory_value,
        inventory_by_category,
        most_frequent_customers,
        average_customer_ticket,
        preferred_payment_methods,
        revenue_by_supplier,
        sales_vs_inventory_by_category,
    ]
    tool_node = ToolNode(tools)

    # LLM + tools (habilita tool calling)
    llm = _get_llm().bind_tools(tools)

    system_msg = SystemMessage(content=_load_system_prompt())

    def agent_node(state: AgentState) -> dict:
        logger.info("🧠 [AGENT] Ejecutando agente principal")

        msgs = state["messages"]
        user_query = ""
        
        if not msgs or not isinstance(msgs[0], SystemMessage):
            logger.debug("🧠 [AGENT] Inyectando SystemPrompt")
            msgs = [system_msg] + msgs
            if len(msgs) > 1:
                user_query = msgs[1].content if hasattr(msgs[1], 'content') else ""
        else:
            if len(msgs) > 1:
                user_query = msgs[1].content if hasattr(msgs[1], 'content') else ""

        logger.debug(f"🧠 [AGENT] Mensajes actuales: {len(msgs)}")
        logger.debug(f"🧠 [AGENT] Query del usuario: {user_query[:100]}")

        # Detectar si ya hubo un tool_call (revisar TODOS los mensajes previos del estado)
        from langchain_core.messages import ToolMessage
        for msg in state["messages"][-5:]:  # Últimos 5 mensajes
            if isinstance(msg, ToolMessage):
                logger.info("✅ [AGENT] ToolMessage detectado, retornando sin LLM")
                # Retornar todo lo que tenemos
                return {"messages": state["messages"]}

        # ESTRATEGIA: Intent matching automático
        # Detectar qué herramienta necesita basado en la query del usuario
        auto_tool = _detect_tool_from_intent(user_query)
        
        if auto_tool:
            logger.info(f"🎯 [AGENT] Intent detectado: {auto_tool['tool_name']}")
            # Crear un AIMessage con tool_calls ya asignados
            ai_msg = AIMessage(
                content=f"Ejecutando herramienta: {auto_tool['tool_name']}",
                tool_calls=[{
                    'name': auto_tool['tool_name'],
                    'args': auto_tool['parameters'],
                    'id': str(uuid4()),
                    'type': 'tool_call'
                }]
            )
            logger.info(f"🔧 [AGENT] Tool asignada directamente: {auto_tool['tool_name']}({auto_tool['parameters']})")
            return {"messages": [ai_msg]}
        
        # Si no se detectó intent, llamar al LLM normalmente
        logger.info("📝 [AGENT] No se detectó intent específico, usando LLM")
        ai_msg = llm.invoke(msgs)

        if getattr(ai_msg, "tool_calls", None):
            logger.info("🔧 [AGENT] El modelo generó tool_calls")
        else:
            logger.info("🧠 [AGENT] El modelo respondió directamente (sin tools)")

        return {"messages": [ai_msg]}


    def should_continue(state: AgentState) -> str:
        last = state["messages"][-1]

        if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
            logger.info("➡️ [GRAPH] Transición a nodo TOOLS")
            return "tools"

        logger.info("⏹️ [GRAPH] Finalizando ejecución del grafo")
        return "end"


    g = StateGraph(AgentState)

    g.add_node("agent", agent_node)
    g.add_node("tools", tool_node)

    g.set_entry_point("agent")
    g.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
    g.add_edge("tools", "agent")

    app = g.compile()

    if save_diagram:
        _save_mermaid_diagram(app)

    return app


def _save_mermaid_diagram(compiled_graph):
    """
    Exporta un diagrama Mermaid del grafo en /artifacts/graph.mmd
    """
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = repo_root / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "graph.mmd"
    try:
        mermaid = compiled_graph.get_graph().draw_mermaid()
        out_path.write_text(mermaid, encoding="utf-8")
    except Exception as e:
        out_path.write_text(
            f"%% No pude generar Mermaid automáticamente.\n%% Error: {type(e).__name__}: {e}\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    _ = build_graph(save_diagram=True)
    print("OK: grafo compilado y diagrama guardado en artifacts/graph.mmd")
