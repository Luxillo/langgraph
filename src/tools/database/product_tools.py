"""Simple product tools that use the project's DB connection helper.

These are minimal helpers to be used by higher-level tools or for testing.
"""
from typing import List
from langchain_core.tools import tool
from src.database.connection import execute_query


@tool("search_products_by_name")
def search_products_by_name(term: str, limit: int = 25) -> List[dict]:
    """
    Busca productos por nombre (insensible a mayúsculas/minúsculas).
    Retorna lista de diccionarios con id, nombre, marca, stock y precio.
    Uso: cuando el usuario pregunta por un producto específico.
    """
    sql = "SELECT id, nombre AS name, marca AS brand, grupo AS category, precio_unidad AS price, stock FROM productos WHERE lower(nombre) LIKE lower(:pat) ORDER BY id LIMIT :limit"
    params = {"pat": f"%{term}%", "limit": limit}
    return execute_query(sql, params)


@tool("get_low_stock_products")
def get_low_stock_products(threshold: int = 10) -> List[dict]:
    """
    Retorna productos con stock igual o menor al 'threshold' (umbral).
    Uso: para detectar productos agotados o con poco inventario.
    """
    sql = "SELECT id, nombre AS name, marca AS brand, grupo AS category, stock FROM productos WHERE stock <= :threshold ORDER BY stock ASC"
    return execute_query(sql, {"threshold": threshold})
