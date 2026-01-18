"""Supermarket models."""

from pydantic import BaseModel, Field


class DeliveryCost(BaseModel):
    """Delivery cost details."""

    delivery_cost: float = Field(0.0, description="Base delivery cost")
    free_delivery_threshold: float | None = Field(
        None, description="Order amount for free delivery"
    )
    pickup_available: bool = Field(False, description="Pickup available")
    pickup_cost: float = Field(0.0, description="Pickup cost")


class SupermarketBase(BaseModel):
    """Base supermarket model."""

    name: str = Field(..., description="Internal name (e.g., albert_heijn)")
    display_name: str = Field(..., description="Display name (e.g., Albert Heijn)")
    base_url: str = Field(..., description="Base URL of the supermarket")
    delivery_cost: float = Field(0.0, description="Delivery cost")
    free_delivery_threshold: float | None = Field(None)
    pickup_available: bool = Field(False)
    pickup_cost: float = Field(0.0)
    has_bonus_card: bool = Field(False)
    bonus_card_name: str | None = Field(None)


class SupermarketCreate(SupermarketBase):
    """Model for creating a supermarket."""

    pass


class Supermarket(SupermarketBase):
    """Supermarket model with ID."""

    id: int

    class Config:
        from_attributes = True
