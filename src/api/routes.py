"""FastAPI routes for the price comparison API."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from loguru import logger

from src.services.price_service import PriceService
from src.database import get_db
from src.database.crud import (
    get_all_supermarkets,
    get_all_shopping_lists,
    create_shopping_list,
    add_item_to_list,
    delete_shopping_list,
)

router = APIRouter(prefix="/api", tags=["api"])


class SearchRequest(BaseModel):
    """Search request model."""

    query: str


class ShoppingListRequest(BaseModel):
    """Shopping list request model."""

    name: str


class ShoppingItemRequest(BaseModel):
    """Shopping item request model."""

    product_name: str
    quantity: int = 1


class CompareRequest(BaseModel):
    """Compare request model."""

    items: list[dict]
    has_bonus_card: bool = True


@router.get("/supermarkets")
async def list_supermarkets():
    """Get all supermarkets."""
    db_manager = get_db()
    with db_manager.get_session() as session:
        supermarkets = get_all_supermarkets(session)
        return [
            {
                "id": s.id,
                "name": s.name,
                "display_name": s.display_name,
                "delivery_cost": s.delivery_cost,
                "free_delivery_threshold": s.free_delivery_threshold,
                "pickup_available": s.pickup_available,
                "has_bonus_card": s.has_bonus_card,
                "bonus_card_name": s.bonus_card_name,
            }
            for s in supermarkets
        ]


@router.post("/search")
async def search_products(request: SearchRequest):
    """Search for products across all supermarkets."""
    price_service = PriceService()
    try:
        results = await price_service.search_and_compare(request.query)
        return {"query": request.query, "results": results}
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare")
async def compare_shopping_list(request: CompareRequest):
    """Compare shopping list across supermarkets."""
    price_service = PriceService()
    try:
        options = await price_service.compare_shopping_list(
            request.items, request.has_bonus_card
        )
        return {
            "options": [opt.model_dump() for opt in options],
            "cheapest": options[0].model_dump() if options else None,
        }
    except Exception as e:
        logger.error(f"Compare error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/shopping-lists")
async def list_shopping_lists():
    """Get all shopping lists."""
    db_manager = get_db()
    with db_manager.get_session() as session:
        lists = get_all_shopping_lists(session)
        return [
            {
                "id": sl.id,
                "name": sl.name,
                "created_at": sl.created_at.isoformat(),
                "items": [
                    {"id": item.id, "name": item.product_name, "quantity": item.quantity}
                    for item in sl.items
                ],
            }
            for sl in lists
        ]


@router.post("/shopping-lists")
async def create_list(request: ShoppingListRequest):
    """Create a new shopping list."""
    db_manager = get_db()
    with db_manager.get_session() as session:
        shopping_list = create_shopping_list(session, request.name)
        return {"id": shopping_list.id, "name": shopping_list.name}


@router.post("/shopping-lists/{list_id}/items")
async def add_item(list_id: int, request: ShoppingItemRequest):
    """Add item to shopping list."""
    db_manager = get_db()
    with db_manager.get_session() as session:
        item = add_item_to_list(
            session, list_id, request.product_name, request.quantity
        )
        return {"id": item.id, "name": item.product_name, "quantity": item.quantity}


@router.delete("/shopping-lists/{list_id}")
async def delete_list(list_id: int):
    """Delete a shopping list."""
    db_manager = get_db()
    with db_manager.get_session() as session:
        success = delete_shopping_list(session, list_id)
        if not success:
            raise HTTPException(status_code=404, detail="Shopping list not found")
        return {"success": True}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
