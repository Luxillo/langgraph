from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from src.tools.database.product_tools import search_products_by_name, get_low_stock_products

router = APIRouter(prefix="/tools/db", tags=["db-tools"])


class SearchRequest(BaseModel):
    term: str
    limit: int = 25


class LowStockRequest(BaseModel):
    threshold: int = 10


@router.post("/search_products")
def search_products(req: SearchRequest) -> List[dict]:
    """Search products by name (wrapper for testing)."""
    return search_products_by_name(req.term, limit=req.limit)


@router.post("/low_stock")
def low_stock(req: LowStockRequest) -> List[dict]:
    """Return products with low stock (wrapper for testing)."""
    return get_low_stock_products(req.threshold)
