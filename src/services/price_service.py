"""Price service for price comparison functionality."""

from loguru import logger

from src.database import get_db
from src.database.crud import (
    get_all_supermarkets,
    search_products,
    get_latest_prices,
)
from src.services.scraper_service import ScraperService
from src.services.product_matcher import ProductMatcherService
from src.services.cost_calculator import CostCalculatorService
from src.models.supermarket import Supermarket
from src.models.price import PriceComparison
from src.models.shopping_list import ShoppingListComparison


class PriceService:
    """High-level service for price comparison operations."""

    def __init__(self):
        """Initialize price service."""
        self.scraper_service = ScraperService()
        self.matcher_service = ProductMatcherService()
        self.calculator_service = CostCalculatorService()

    async def search_and_compare(
        self, query: str
    ) -> dict[str, dict]:
        """Search for a product and compare prices across supermarkets."""
        # Search all supermarkets
        results = await self.scraper_service.search_all_supermarkets(query)

        # Match products across stores
        comparison = self.matcher_service.get_price_comparison(query, results)

        return comparison

    async def compare_shopping_list(
        self,
        items: list[dict],
        has_bonus_card: bool = True,
    ) -> list[ShoppingListComparison]:
        """Compare total cost for a shopping list across supermarkets."""
        # Get supermarkets from database
        db_manager = get_db()
        with db_manager.get_session() as session:
            supermarkets_db = get_all_supermarkets(session)

            supermarkets = [
                Supermarket(
                    id=s.id,
                    name=s.name,
                    display_name=s.display_name,
                    base_url=s.base_url,
                    delivery_cost=s.delivery_cost,
                    free_delivery_threshold=s.free_delivery_threshold,
                    pickup_available=s.pickup_available,
                    pickup_cost=s.pickup_cost,
                    has_bonus_card=s.has_bonus_card,
                    bonus_card_name=s.bonus_card_name,
                )
                for s in supermarkets_db
            ]

        # For each item, get prices from all supermarkets
        enriched_items = []
        for item in items:
            product_name = item.get("product_name", item.get("name", ""))
            quantity = item.get("quantity", 1)

            # Search for product prices
            results = await self.scraper_service.search_all_supermarkets(
                product_name
            )
            comparison = self.matcher_service.get_price_comparison(
                product_name, results
            )

            # Extract best prices per supermarket
            prices = {}
            for supermarket, data in comparison.items():
                if data:
                    prices[supermarket] = data.get("best_price", 0)

            enriched_items.append({
                "product_name": product_name,
                "quantity": quantity,
                "prices": prices,
            })

        # Compare all options
        options = self.calculator_service.compare_all_options(
            enriched_items, supermarkets, has_bonus_card
        )

        return options

    def get_price_history(
        self, product_name: str, days: int = 30
    ) -> dict[str, list]:
        """Get price history for a product."""
        db_manager = get_db()

        with db_manager.get_session() as session:
            products = search_products(session, product_name, limit=5)

            if not products:
                return {}

            history = {}
            for product in products:
                prices = get_latest_prices(session, product.id)
                history[product.name] = [
                    {
                        "supermarket": p.supermarket.display_name,
                        "price": p.regular_price,
                        "sale_price": p.sale_price,
                        "bonus_price": p.bonus_card_price,
                        "date": p.scraped_at.isoformat(),
                    }
                    for p in prices
                ]

            return history

    def get_cheapest_supermarket(
        self, items: list[dict], has_bonus_card: bool = True
    ) -> str | None:
        """Get the name of the cheapest supermarket for a shopping list."""
        import asyncio

        options = asyncio.run(
            self.compare_shopping_list(items, has_bonus_card)
        )

        if options:
            return options[0].supermarket
        return None
