"""Scraper service for orchestrating supermarket scrapers."""

import asyncio
from typing import Any
from loguru import logger

from src.scrapers import (
    AlbertHeijnScraper,
    JumboScraper,
    DirkScraper,
    PlusScraper,
    FlinkScraper,
    PicnicScraper,
)
from src.models.product import ProductSearch
from src.database import get_db
from src.database.crud import (
    get_or_create_product,
    create_price_record,
    get_supermarket_by_name,
)


class ScraperService:
    """Service for managing and orchestrating scrapers."""

    def __init__(self):
        """Initialize scraper service with all scrapers."""
        self.scrapers = {
            "albert_heijn": AlbertHeijnScraper(),
            "jumbo": JumboScraper(),
            "dirk": DirkScraper(),
            "plus": PlusScraper(),
            "flink": FlinkScraper(),
            "picnic": PicnicScraper(),
        }

    async def search_all_supermarkets(
        self, query: str
    ) -> dict[str, list[ProductSearch]]:
        """Search for products in all supermarkets concurrently."""
        tasks = {
            name: asyncio.create_task(scraper.search_product(query))
            for name, scraper in self.scrapers.items()
        }

        results: dict[str, list[ProductSearch]] = {}

        for name, task in tasks.items():
            try:
                result = await task
                results[name] = result
                logger.info(f"{name}: {len(result)} results")
            except Exception as e:
                logger.error(f"Error searching {name}: {e}")
                results[name] = []

        return results

    async def search_supermarket(
        self, supermarket: str, query: str
    ) -> list[ProductSearch]:
        """Search for products in a specific supermarket."""
        if supermarket not in self.scrapers:
            logger.error(f"Unknown supermarket: {supermarket}")
            return []

        try:
            return await self.scrapers[supermarket].search_product(query)
        except Exception as e:
            logger.error(f"Error searching {supermarket}: {e}")
            return []

    def save_search_results(
        self, results: dict[str, list[ProductSearch]]
    ) -> int:
        """Save search results to database."""
        db_manager = get_db()
        saved_count = 0

        with db_manager.get_session() as session:
            for supermarket_name, products in results.items():
                supermarket = get_supermarket_by_name(session, supermarket_name)
                if not supermarket:
                    logger.warning(f"Supermarket not found: {supermarket_name}")
                    continue

                for product_data in products:
                    try:
                        # Get or create product
                        product = get_or_create_product(
                            session,
                            name=product_data.name,
                            brand=product_data.brand,
                            unit=product_data.unit,
                            unit_size=product_data.unit_size,
                            image_url=product_data.image_url,
                        )

                        # Create price record
                        create_price_record(
                            session,
                            product_id=product.id,
                            supermarket_id=supermarket.id,
                            regular_price=product_data.regular_price,
                            sale_price=product_data.sale_price,
                            bonus_card_price=product_data.bonus_card_price,
                            promotion_text=product_data.promotion_text,
                            url=product_data.url,
                        )
                        saved_count += 1

                    except Exception as e:
                        logger.error(f"Error saving product: {e}")
                        continue

        logger.info(f"Saved {saved_count} price records")
        return saved_count


# Module-level runner for command line usage
async def main():
    """Run scraper service from command line."""
    service = ScraperService()

    # Example: search for common products
    queries = ["melk", "brood", "kaas", "eieren", "appels"]

    for query in queries:
        logger.info(f"Searching for: {query}")
        results = await service.search_all_supermarkets(query)
        service.save_search_results(results)


if __name__ == "__main__":
    asyncio.run(main())
