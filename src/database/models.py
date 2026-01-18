"""SQLAlchemy database models."""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class SupermarketDB(Base):
    """Supermarket database model."""

    __tablename__ = "supermarkets"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    display_name = Column(String, nullable=False)
    base_url = Column(String, nullable=False)
    delivery_cost = Column(Float, default=0.0)
    free_delivery_threshold = Column(Float, nullable=True)
    pickup_available = Column(Boolean, default=False)
    pickup_cost = Column(Float, default=0.0)
    has_bonus_card = Column(Boolean, default=False)
    bonus_card_name = Column(String, nullable=True)

    # Relationships
    price_records = relationship("PriceRecordDB", back_populates="supermarket")


class ProductDB(Base):
    """Product database model."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=True)
    category = Column(String, nullable=True)
    unit = Column(String, default="stuk")
    unit_size = Column(Float, default=1.0)
    image_url = Column(String, nullable=True)

    # Relationships
    price_records = relationship("PriceRecordDB", back_populates="product")

    __table_args__ = (Index("ix_products_name_brand", "name", "brand"),)


class PriceRecordDB(Base):
    """Price record database model."""

    __tablename__ = "price_records"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    supermarket_id = Column(Integer, ForeignKey("supermarkets.id"), nullable=False)
    regular_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=True)
    bonus_card_price = Column(Float, nullable=True)
    promotion_text = Column(String, nullable=True)
    promotion_type = Column(String, nullable=True)
    url = Column(String, nullable=False)
    scraped_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("ProductDB", back_populates="price_records")
    supermarket = relationship("SupermarketDB", back_populates="price_records")

    __table_args__ = (
        Index("ix_price_records_product_supermarket", "product_id", "supermarket_id"),
        Index("ix_price_records_scraped_at", "scraped_at"),
    )


class FavoriteProductDB(Base):
    """Favorite product database model."""

    __tablename__ = "favorite_products"

    id = Column(Integer, primary_key=True)
    user_query = Column(String, nullable=False)
    matched_product_ids = Column(JSON, default=dict)
    preferred_brand = Column(String, nullable=True)
    min_quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)


class ShoppingListDB(Base):
    """Shopping list database model."""

    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    items = relationship(
        "ShoppingListItemDB", back_populates="shopping_list", cascade="all, delete"
    )


class ShoppingListItemDB(Base):
    """Shopping list item database model."""

    __tablename__ = "shopping_list_items"

    id = Column(Integer, primary_key=True)
    shopping_list_id = Column(
        Integer, ForeignKey("shopping_lists.id"), nullable=False
    )
    favorite_product_id = Column(
        Integer, ForeignKey("favorite_products.id"), nullable=True
    )
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)

    # Relationships
    shopping_list = relationship("ShoppingListDB", back_populates="items")
