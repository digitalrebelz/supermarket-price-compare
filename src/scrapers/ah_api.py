"""Albert Heijn scraper using official mobile API via SupermarktConnector."""

from loguru import logger
from supermarktconnector.ah import AHConnector

from src.models.product import ProductSearch


class AlbertHeijnAPIScraper:
    """Scraper for Albert Heijn using their mobile API."""

    def __init__(self):
        """Initialize AH API scraper."""
        self.connector = AHConnector()
        self.supermarket_name = "albert_heijn"

    def search_product(self, query: str, limit: int = 10) -> list[ProductSearch]:
        """Search for products using AH mobile API."""
        results: list[ProductSearch] = []

        try:
            response = self.connector.search_products(query=query, size=limit, page=0)

            if not response or "products" not in response:
                logger.warning(f"AH API: No products found for '{query}'")
                return results

            for product in response["products"]:
                try:
                    # Extract product data
                    title = product.get("title", "Unknown")

                    # Price handling - AH uses priceBeforeBonus for regular, currentPrice for bonus
                    price_before = product.get("priceBeforeBonus")
                    current_price = product.get("currentPrice", 0)

                    if price_before:
                        regular_price = price_before
                        bonus_price = current_price
                    else:
                        regular_price = current_price
                        bonus_price = None

                    # Build product URL
                    webshop_id = product.get("webshopId", "")
                    url = f"https://www.ah.nl/producten/product/{webshop_id}" if webshop_id else ""

                    # Get image
                    images = product.get("images", [])
                    image_url = images[0].get("url") if images else None

                    # Extract unit info
                    unit_size = product.get("unitSize", "")

                    results.append(
                        ProductSearch(
                            name=title,
                            brand=product.get("brand"),
                            regular_price=regular_price,
                            bonus_card_price=bonus_price,
                            promotion_text=product.get("discountLabel"),
                            url=url,
                            image_url=image_url,
                            unit="stuk",
                            unit_size=1.0,
                            supermarket=self.supermarket_name,
                        )
                    )

                except Exception as e:
                    logger.debug(f"Error parsing AH product: {e}")
                    continue

            logger.info(f"AH API: Found {len(results)} products for '{query}'")

        except Exception as e:
            logger.error(f"AH API error: {e}")

        return results

    def get_product_details(self, product_id: str) -> ProductSearch | None:
        """Get detailed product information."""
        try:
            product = self.connector.get_product_details(product_id)
            if product:
                return ProductSearch(
                    name=product.get("title", "Unknown"),
                    regular_price=product.get("currentPrice", 0),
                    url=f"https://www.ah.nl/producten/product/{product_id}",
                    supermarket=self.supermarket_name,
                )
        except Exception as e:
            logger.error(f"Error getting AH product details: {e}")
        return None
