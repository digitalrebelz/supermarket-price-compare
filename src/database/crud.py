"""CRUD operations for database models."""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from loguru import logger

from src.database.models import (
    SupermarketDB,
    ProductDB,
    PriceRecordDB,
    FavoriteProductDB,
    ShoppingListDB,
    ShoppingListItemDB,
)


# Supermarket CRUD
def get_supermarket_by_name(db: Session, name: str) -> SupermarketDB | None:
    """Get supermarket by internal name."""
    return db.query(SupermarketDB).filter(SupermarketDB.name == name).first()


def get_all_supermarkets(db: Session) -> list[SupermarketDB]:
    """Get all supermarkets."""
    return db.query(SupermarketDB).all()


def create_supermarket(db: Session, **kwargs) -> SupermarketDB:
    """Create a new supermarket."""
    supermarket = SupermarketDB(**kwargs)
    db.add(supermarket)
    db.flush()
    return supermarket


def upsert_supermarket(db: Session, **kwargs) -> SupermarketDB:
    """Create or update a supermarket."""
    existing = get_supermarket_by_name(db, kwargs["name"])
    if existing:
        for key, value in kwargs.items():
            setattr(existing, key, value)
        db.flush()
        return existing
    return create_supermarket(db, **kwargs)


# Product CRUD
def get_product_by_id(db: Session, product_id: int) -> ProductDB | None:
    """Get product by ID."""
    return db.query(ProductDB).filter(ProductDB.id == product_id).first()


def search_products(
    db: Session, query: str, limit: int = 20
) -> list[ProductDB]:
    """Search products by name."""
    return (
        db.query(ProductDB)
        .filter(ProductDB.name.ilike(f"%{query}%"))
        .limit(limit)
        .all()
    )


def create_product(db: Session, **kwargs) -> ProductDB:
    """Create a new product."""
    product = ProductDB(**kwargs)
    db.add(product)
    db.flush()
    return product


def get_or_create_product(
    db: Session, name: str, brand: str | None = None, **kwargs
) -> ProductDB:
    """Get existing product or create new one."""
    query = db.query(ProductDB).filter(ProductDB.name == name)
    if brand:
        query = query.filter(ProductDB.brand == brand)
    existing = query.first()
    if existing:
        return existing
    return create_product(db, name=name, brand=brand, **kwargs)


# Price Record CRUD
def create_price_record(db: Session, **kwargs) -> PriceRecordDB:
    """Create a new price record."""
    record = PriceRecordDB(**kwargs)
    db.add(record)
    db.flush()
    return record


def get_latest_prices(
    db: Session, product_id: int
) -> list[PriceRecordDB]:
    """Get latest prices for a product from all supermarkets."""
    subquery = (
        db.query(
            PriceRecordDB.supermarket_id,
            db.func.max(PriceRecordDB.scraped_at).label("max_scraped"),
        )
        .filter(PriceRecordDB.product_id == product_id)
        .group_by(PriceRecordDB.supermarket_id)
        .subquery()
    )

    return (
        db.query(PriceRecordDB)
        .join(
            subquery,
            and_(
                PriceRecordDB.supermarket_id == subquery.c.supermarket_id,
                PriceRecordDB.scraped_at == subquery.c.max_scraped,
            ),
        )
        .filter(PriceRecordDB.product_id == product_id)
        .all()
    )


def get_prices_by_supermarket(
    db: Session, supermarket_id: int, limit: int = 100
) -> list[PriceRecordDB]:
    """Get recent prices for a supermarket."""
    return (
        db.query(PriceRecordDB)
        .filter(PriceRecordDB.supermarket_id == supermarket_id)
        .order_by(PriceRecordDB.scraped_at.desc())
        .limit(limit)
        .all()
    )


# Favorite Product CRUD
def create_favorite_product(db: Session, **kwargs) -> FavoriteProductDB:
    """Create a new favorite product."""
    favorite = FavoriteProductDB(**kwargs)
    db.add(favorite)
    db.flush()
    return favorite


def get_all_favorites(db: Session) -> list[FavoriteProductDB]:
    """Get all favorite products."""
    return db.query(FavoriteProductDB).all()


def delete_favorite(db: Session, favorite_id: int) -> bool:
    """Delete a favorite product."""
    favorite = (
        db.query(FavoriteProductDB)
        .filter(FavoriteProductDB.id == favorite_id)
        .first()
    )
    if favorite:
        db.delete(favorite)
        return True
    return False


# Shopping List CRUD
def create_shopping_list(db: Session, name: str) -> ShoppingListDB:
    """Create a new shopping list."""
    shopping_list = ShoppingListDB(name=name)
    db.add(shopping_list)
    db.flush()
    return shopping_list


def get_shopping_list(db: Session, list_id: int) -> ShoppingListDB | None:
    """Get shopping list by ID."""
    return (
        db.query(ShoppingListDB)
        .filter(ShoppingListDB.id == list_id)
        .first()
    )


def get_all_shopping_lists(db: Session) -> list[ShoppingListDB]:
    """Get all shopping lists."""
    return db.query(ShoppingListDB).order_by(ShoppingListDB.created_at.desc()).all()


def add_item_to_list(
    db: Session, list_id: int, product_name: str, quantity: int = 1
) -> ShoppingListItemDB:
    """Add item to shopping list."""
    item = ShoppingListItemDB(
        shopping_list_id=list_id,
        product_name=product_name,
        quantity=quantity,
    )
    db.add(item)
    db.flush()
    return item


def remove_item_from_list(db: Session, item_id: int) -> bool:
    """Remove item from shopping list."""
    item = (
        db.query(ShoppingListItemDB)
        .filter(ShoppingListItemDB.id == item_id)
        .first()
    )
    if item:
        db.delete(item)
        return True
    return False


def update_item_quantity(db: Session, item_id: int, quantity: int) -> bool:
    """Update item quantity."""
    item = (
        db.query(ShoppingListItemDB)
        .filter(ShoppingListItemDB.id == item_id)
        .first()
    )
    if item:
        item.quantity = quantity
        return True
    return False


def delete_shopping_list(db: Session, list_id: int) -> bool:
    """Delete a shopping list."""
    shopping_list = get_shopping_list(db, list_id)
    if shopping_list:
        db.delete(shopping_list)
        return True
    return False
