"""Unit tests for database operations."""

import pytest
from datetime import datetime

from src.database.crud import (
    create_supermarket,
    get_supermarket_by_name,
    get_all_supermarkets,
    upsert_supermarket,
    create_product,
    get_product_by_id,
    search_products,
    get_or_create_product,
    create_price_record,
    get_latest_prices,
    create_shopping_list,
    add_item_to_list,
    get_shopping_list,
    delete_shopping_list,
)


class TestSupermarketCRUD:
    """Tests for supermarket CRUD operations."""

    def test_create_supermarket(self, db_session, sample_supermarket_data):
        """Test creating a supermarket."""
        supermarket = create_supermarket(
            db_session,
            name=sample_supermarket_data["name"],
            display_name=sample_supermarket_data["display_name"],
            base_url=sample_supermarket_data["base_url"],
            delivery_cost=sample_supermarket_data["delivery_cost"],
        )

        assert supermarket.id is not None
        assert supermarket.name == "albert_heijn"
        assert supermarket.display_name == "Albert Heijn"

    def test_get_supermarket_by_name(self, db_session, sample_supermarket_data):
        """Test getting supermarket by name."""
        create_supermarket(
            db_session,
            name=sample_supermarket_data["name"],
            display_name=sample_supermarket_data["display_name"],
            base_url=sample_supermarket_data["base_url"],
        )

        result = get_supermarket_by_name(db_session, "albert_heijn")
        assert result is not None
        assert result.name == "albert_heijn"

    def test_get_supermarket_by_name_not_found(self, db_session):
        """Test getting non-existent supermarket."""
        result = get_supermarket_by_name(db_session, "nonexistent")
        assert result is None

    def test_get_all_supermarkets(self, db_session):
        """Test getting all supermarkets."""
        create_supermarket(db_session, name="ah", display_name="AH", base_url="https://ah.nl")
        create_supermarket(db_session, name="jumbo", display_name="Jumbo", base_url="https://jumbo.com")

        supermarkets = get_all_supermarkets(db_session)
        assert len(supermarkets) == 2

    def test_upsert_supermarket_create(self, db_session):
        """Test upsert creates new supermarket."""
        supermarket = upsert_supermarket(
            db_session,
            name="new_store",
            display_name="New Store",
            base_url="https://new.com",
        )

        assert supermarket.id is not None
        assert supermarket.name == "new_store"

    def test_upsert_supermarket_update(self, db_session):
        """Test upsert updates existing supermarket."""
        create_supermarket(
            db_session,
            name="store",
            display_name="Old Name",
            base_url="https://old.com",
        )

        updated = upsert_supermarket(
            db_session,
            name="store",
            display_name="New Name",
            base_url="https://new.com",
        )

        assert updated.display_name == "New Name"
        assert updated.base_url == "https://new.com"


class TestProductCRUD:
    """Tests for product CRUD operations."""

    def test_create_product(self, db_session, sample_product_data):
        """Test creating a product."""
        product = create_product(db_session, **sample_product_data)

        assert product.id is not None
        assert product.name == "Melk halfvol 1L"
        assert product.brand == "Campina"

    def test_get_product_by_id(self, db_session, sample_product_data):
        """Test getting product by ID."""
        created = create_product(db_session, **sample_product_data)
        result = get_product_by_id(db_session, created.id)

        assert result is not None
        assert result.id == created.id

    def test_search_products(self, db_session):
        """Test searching products."""
        create_product(db_session, name="Halfvolle Melk", unit="liter")
        create_product(db_session, name="Volle Melk", unit="liter")
        create_product(db_session, name="Brood", unit="stuk")

        results = search_products(db_session, "Melk")
        assert len(results) == 2

    def test_get_or_create_product_create(self, db_session):
        """Test get_or_create creates new product."""
        product = get_or_create_product(
            db_session,
            name="New Product",
            brand="Brand",
            unit="stuk",
        )

        assert product.id is not None
        assert product.name == "New Product"

    def test_get_or_create_product_get(self, db_session):
        """Test get_or_create returns existing product."""
        created = create_product(
            db_session,
            name="Existing Product",
            brand="Brand",
            unit="stuk",
        )

        result = get_or_create_product(
            db_session,
            name="Existing Product",
            brand="Brand",
        )

        assert result.id == created.id


class TestPriceRecordCRUD:
    """Tests for price record CRUD operations."""

    def test_create_price_record(self, db_session, sample_price_data):
        """Test creating a price record."""
        # Create required foreign key records
        supermarket = create_supermarket(
            db_session, name="ah", display_name="AH", base_url="https://ah.nl"
        )
        product = create_product(db_session, name="Test Product", unit="stuk")

        record = create_price_record(
            db_session,
            product_id=product.id,
            supermarket_id=supermarket.id,
            **sample_price_data,
        )

        assert record.id is not None
        assert record.regular_price == 1.49
        assert record.bonus_card_price == 0.99


class TestShoppingListCRUD:
    """Tests for shopping list CRUD operations."""

    def test_create_shopping_list(self, db_session):
        """Test creating a shopping list."""
        shopping_list = create_shopping_list(db_session, "Weekly Groceries")

        assert shopping_list.id is not None
        assert shopping_list.name == "Weekly Groceries"

    def test_add_item_to_list(self, db_session):
        """Test adding item to shopping list."""
        shopping_list = create_shopping_list(db_session, "Test List")
        item = add_item_to_list(db_session, shopping_list.id, "Milk", 2)

        assert item.id is not None
        assert item.product_name == "Milk"
        assert item.quantity == 2

    def test_get_shopping_list(self, db_session):
        """Test getting shopping list."""
        created = create_shopping_list(db_session, "Test List")
        add_item_to_list(db_session, created.id, "Milk", 2)

        result = get_shopping_list(db_session, created.id)

        assert result is not None
        assert len(result.items) == 1

    def test_delete_shopping_list(self, db_session):
        """Test deleting shopping list."""
        shopping_list = create_shopping_list(db_session, "To Delete")
        success = delete_shopping_list(db_session, shopping_list.id)

        assert success
        assert get_shopping_list(db_session, shopping_list.id) is None
