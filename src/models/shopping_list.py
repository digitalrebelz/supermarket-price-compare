"""Shopping list models."""

from datetime import datetime
from pydantic import BaseModel, Field


class ShoppingItem(BaseModel):
    """Single item in a shopping list."""

    product_name: str
    quantity: int = Field(1, ge=1)
    preferred_brand: str | None = None
    matched_product_ids: dict[str, int] = Field(
        default_factory=dict, description="Product IDs per supermarket"
    )


class ShoppingListBase(BaseModel):
    """Base shopping list model."""

    name: str = Field(..., description="List name")
    items: list[ShoppingItem] = Field(default_factory=list)


class ShoppingListCreate(ShoppingListBase):
    """Model for creating a shopping list."""

    pass


class ShoppingList(ShoppingListBase):
    """Shopping list model with ID and timestamp."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ShoppingListComparison(BaseModel):
    """Shopping list comparison across supermarkets."""

    supermarket: str
    delivery_method: str  # "delivery" or "pickup"
    product_total: float
    delivery_cost: float
    total: float
    items: list[dict]
    savings: float  # compared to most expensive option
    is_cheapest: bool = False
