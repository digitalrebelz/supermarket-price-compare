"""Picnic scraper."""

from urllib.parse import quote
from loguru import logger

from src.scrapers.base_scraper import BaseScraper
from src.models.product import ProductSearch


class PicnicScraper(BaseScraper):
    """Scraper for Picnic online supermarket."""

    def __init__(self):
        """Initialize Picnic scraper."""
        super().__init__("picnic")

    async def search_product(self, query: str) -> list[ProductSearch]:
        """Search for products on Picnic website."""
        results: list[ProductSearch] = []
        playwright = None
        browser = None

        try:
            playwright, browser = await self._create_browser()
            page = await self._create_page(browser)

            # Navigate to search page
            search_url = self.config["search_url"].format(query=quote(query))
            await self._fetch_page(page, search_url)

            # Accept cookies
            await self._accept_cookies(page)

            # Wait for products to load
            try:
                await page.wait_for_selector(
                    self.config["selectors"]["product_card"],
                    timeout=10000,
                )
            except Exception:
                logger.warning(f"No products found for query: {query}")
                return results

            # Extract product data
            products = await page.query_selector_all(
                self.config["selectors"]["product_card"]
            )

            for product in products[:10]:
                try:
                    # Get product title
                    title_el = await product.query_selector(
                        self.config["selectors"]["product_title"]
                    )
                    name = await title_el.inner_text() if title_el else None

                    if not name:
                        continue

                    # Get price
                    price_el = await product.query_selector(
                        self.config["selectors"]["product_price"]
                    )
                    price_text = await price_el.inner_text() if price_el else "0"
                    regular_price = self._parse_price(price_text) or 0.0

                    # Get product link
                    link_el = await product.query_selector("a")
                    url = ""
                    if link_el:
                        href = await link_el.get_attribute("href")
                        if href:
                            url = (
                                href
                                if href.startswith("http")
                                else f"{self.config['base_url']}{href}"
                            )

                    # Get image
                    img_el = await product.query_selector("img")
                    image_url = None
                    if img_el:
                        image_url = await img_el.get_attribute("src")

                    # Extract unit info
                    unit, unit_size = self._extract_unit_info(name)

                    results.append(
                        ProductSearch(
                            name=name,
                            regular_price=regular_price,
                            url=url,
                            image_url=image_url,
                            unit=unit,
                            unit_size=unit_size,
                            supermarket=self.supermarket_name,
                        )
                    )

                except Exception as e:
                    logger.debug(f"Error extracting product: {e}")
                    continue

            logger.info(f"Picnic: Found {len(results)} products for '{query}'")

        except Exception as e:
            logger.error(f"Picnic scraping error: {e}")

        finally:
            if browser:
                await browser.close()
            if playwright:
                await playwright.stop()

        return results

    async def get_product_details(self, url: str) -> ProductSearch | None:
        """Get detailed product information from product page."""
        playwright = None
        browser = None

        try:
            playwright, browser = await self._create_browser()
            page = await self._create_page(browser)

            await self._fetch_page(page, url)
            await self._accept_cookies(page)

            name_el = await page.query_selector("h1")
            name = await name_el.inner_text() if name_el else "Unknown"

            price_el = await page.query_selector(".product-price")
            price_text = await price_el.inner_text() if price_el else "0"
            price = self._parse_price(price_text) or 0.0

            unit, unit_size = self._extract_unit_info(name)

            return ProductSearch(
                name=name,
                regular_price=price,
                url=url,
                unit=unit,
                unit_size=unit_size,
                supermarket=self.supermarket_name,
            )

        except Exception as e:
            logger.error(f"Error getting product details: {e}")
            return None

        finally:
            if browser:
                await browser.close()
            if playwright:
                await playwright.stop()
