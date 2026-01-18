"""Price models."""

from datetime import datetime
from pydantic import BaseModel, Field


class Promotion(BaseModel):
    """Promotion details."""

    text: str = Field(..., description="Promotion text (e.g., '2e halve prijs')")
    type: str | None = Field(
        None, description="Promotion type (percentage, multibuy, etc)"
    )
    discount_amount: float | None = Field(None, description="Discount amount")
    min_quantity: int = Field(1, description="Minimum quantity for promotion")


class PriceRecordBase(BaseModel):
    """Base price record model."""

    product_id: int
    supermarket_id: int
    regular_price: float
    sale_price: float | None = None
    bonus_card_price: float | None = None
    promotion_text: str | None = None
    promotion_type: str | None = None
    url: str


class PriceRecordCreate(PriceRecordBase):
    """Model for creating a price record."""

    pass


class PriceRecord(PriceRecordBase):
    """Price record model with ID and timestamp."""

    id: int
    scraped_at: datetime

    class Config:
        from_attributes = True


class PriceComparison(BaseModel):
    """Price comparison result."""

    product_name: str
    prices: dict[str, float]  # supermarket_name -> price
    best_price: float
    best_supermarket: str
    savings: float  # compared to highest price
