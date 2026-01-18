"""Product models."""

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product model."""

    name: str = Field(..., description="Product name")
    brand: str | None = Field(None, description="Product brand")
    category: str | None = Field(None, description="Product category")
    unit: str = Field("stuk", description="Unit type (stuk, kg, liter, etc)")
    unit_size: float = Field(1.0, description="Unit size (500 for grams, etc)")
    image_url: str | None = Field(None, description="Product image URL")


class ProductCreate(ProductBase):
    """Model for creating a product."""

    pass


class Product(ProductBase):
    """Product model with ID."""

    id: int

    class Config:
        from_attributes = True


class ProductSearch(BaseModel):
    """Product search result from scraper."""

    name: str
    brand: str | None = None
    regular_price: float
    sale_price: float | None = None
    bonus_card_price: float | None = None
    promotion_text: str | None = None
    unit: str = "stuk"
    unit_size: float = 1.0
    url: str
    image_url: str | None = None
    supermarket: str
