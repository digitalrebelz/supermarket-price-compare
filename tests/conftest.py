"""Pytest configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.db_manager import DatabaseManager
from src.database.models import Base
from src.config.constants import SUPERMARKETS


@pytest.fixture
def db_manager():
    """Create a test database manager with in-memory SQLite."""
    manager = DatabaseManager(database_url="sqlite:///:memory:")
    manager.create_tables()
    yield manager
    manager.drop_tables()


@pytest.fixture
def db_session(db_manager):
    """Create a test database session."""
    with db_manager.get_session() as session:
        yield session


@pytest.fixture
def sample_supermarket_data():
    """Sample supermarket data for testing."""
    return SUPERMARKETS["albert_heijn"]


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "name": "Melk halfvol 1L",
        "brand": "Campina",
        "category": "Zuivel",
        "unit": "liter",
        "unit_size": 1.0,
        "image_url": "https://example.com/melk.jpg",
    }


@pytest.fixture
def sample_price_data():
    """Sample price data for testing."""
    return {
        "regular_price": 1.49,
        "sale_price": 1.29,
        "bonus_card_price": 0.99,
        "promotion_text": "2e halve prijs",
        "url": "https://www.ah.nl/product/melk",
    }


@pytest.fixture
def sample_shopping_list():
    """Sample shopping list for testing."""
    return [
        {"product_name": "Melk", "quantity": 2, "prices": {"albert_heijn": 1.49, "jumbo": 1.59}},
        {"product_name": "Brood", "quantity": 1, "prices": {"albert_heijn": 2.19, "jumbo": 1.99}},
        {"product_name": "Kaas", "quantity": 1, "prices": {"albert_heijn": 4.99, "jumbo": 5.29}},
    ]


@pytest.fixture
def mock_search_results():
    """Mock search results for testing."""
    from src.models.product import ProductSearch

    return {
        "albert_heijn": [
            ProductSearch(
                name="Campina Halfvolle Melk 1L",
                regular_price=1.49,
                bonus_card_price=0.99,
                url="https://www.ah.nl/product/1",
                supermarket="albert_heijn",
            ),
        ],
        "jumbo": [
            ProductSearch(
                name="Campina Halfvolle Melk 1L",
                regular_price=1.59,
                url="https://www.jumbo.com/product/1",
                supermarket="jumbo",
            ),
        ],
    }
