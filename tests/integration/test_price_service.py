"""Integration tests for PriceService."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.services.price_service import PriceService
from src.models.product import ProductSearch


class TestPriceServiceIntegration:
    """Integration tests for PriceService."""

    @pytest.fixture
    def price_service(self):
        """Create PriceService instance."""
        return PriceService()

    @pytest.fixture
    def mock_scraper_results(self):
        """Mock scraper results."""
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
            "dirk": [
                ProductSearch(
                    name="Campina Halfvolle Melk 1L",
                    regular_price=1.39,
                    url="https://www.dirk.nl/product/1",
                    supermarket="dirk",
                ),
            ],
        }

    @pytest.mark.asyncio
    async def test_search_and_compare(self, price_service, mock_scraper_results):
        """Test search and compare functionality."""
        # Use lower threshold for matching
        price_service.matcher_service.similarity_threshold = 0.3

        with patch.object(
            price_service.scraper_service,
            "search_all_supermarkets",
            new_callable=AsyncMock,
            return_value=mock_scraper_results,
        ):
            comparison = await price_service.search_and_compare("halfvolle melk")

            assert "albert_heijn" in comparison
            assert "jumbo" in comparison
            assert "dirk" in comparison

            # Check AH has bonus price
            assert comparison["albert_heijn"]["best_price"] == 0.99

            # Check Dirk is cheapest regular price
            assert comparison["dirk"]["regular_price"] == 1.39

    def test_product_matching_across_stores(self, price_service, mock_scraper_results):
        """Test that products are matched correctly across stores."""
        # Use lower threshold for matching
        from src.services.product_matcher import ProductMatcherService
        matcher = ProductMatcherService(similarity_threshold=0.3)
        comparison = matcher.get_price_comparison(
            "halfvolle melk", mock_scraper_results
        )

        # All stores should have a match
        for store, data in comparison.items():
            assert data is not None
            assert "Melk" in data["name"]

    def test_cost_calculation_consistency(self, price_service):
        """Test that cost calculations are consistent."""
        items = [
            {
                "product_name": "Melk",
                "quantity": 2,
                "prices": {"albert_heijn": 1.49, "jumbo": 1.59},
            },
        ]

        # Create mock supermarkets
        from src.models.supermarket import Supermarket

        supermarkets = [
            Supermarket(
                id=1,
                name="albert_heijn",
                display_name="Albert Heijn",
                base_url="https://www.ah.nl",
                delivery_cost=5.95,
                free_delivery_threshold=None,
                pickup_available=True,
                pickup_cost=0.0,
                has_bonus_card=True,
                bonus_card_name="Bonuskaart",
            ),
            Supermarket(
                id=2,
                name="jumbo",
                display_name="Jumbo",
                base_url="https://www.jumbo.com",
                delivery_cost=7.95,
                free_delivery_threshold=75.0,
                pickup_available=True,
                pickup_cost=0.0,
                has_bonus_card=True,
                bonus_card_name="Extra's",
            ),
        ]

        options = price_service.calculator_service.compare_all_options(
            items, supermarkets
        )

        # Should have delivery and pickup options for both stores
        assert len(options) == 4

        # Check totals are calculated correctly
        for opt in options:
            assert opt.total == opt.product_total + opt.delivery_cost

        # Should be sorted by total
        totals = [opt.total for opt in options]
        assert totals == sorted(totals)
