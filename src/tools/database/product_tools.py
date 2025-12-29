"""Simple product tools that use the project's DB connection helper.

These are minimal helpers to be used by higher-level tools or for testing.
"""
from typing import List
from src.database.connection import execute_query


def search_products_by_name(term: str, limit: int = 25) -> List[dict]:
    """Search products by name (case-insensitive, partial match)."""
    sql = "SELECT id, nombre AS name, marca AS brand, grupo AS category, precio_unidad AS price, stock FROM productos WHERE lower(nombre) LIKE lower(:pat) ORDER BY id LIMIT :limit"
    params = {"pat": f"%{term}%", "limit": limit}
    return execute_query(sql, params)


def get_low_stock_products(threshold: int = 10) -> List[dict]:
    """Return products with stock less or equal than threshold."""
    sql = "SELECT id, nombre AS name, marca AS brand, grupo AS category, stock FROM productos WHERE stock <= :threshold ORDER BY stock ASC"
    return execute_query(sql, {"threshold": threshold})
