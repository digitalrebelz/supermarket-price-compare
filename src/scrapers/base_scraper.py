"""Base scraper class for all supermarket scrapers."""

import asyncio
import random
import re
from abc import ABC, abstractmethod
from typing import Any

from loguru import logger
from playwright.async_api import async_playwright, Page, Browser
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config.settings import get_settings
from src.config.constants import USER_AGENTS, SUPERMARKETS
from src.models.product import ProductSearch


class BaseScraper(ABC):
    """Abstract base class for supermarket scrapers."""

    def __init__(self, supermarket_name: str):
        """Initialize the scraper."""
        self.supermarket_name = supermarket_name
        self.config = SUPERMARKETS[supermarket_name]
        self.settings = get_settings()
        self.rate_limit_delay = self.settings.scrape_rate_limit

    @abstractmethod
    async def search_product(self, query: str) -> list[ProductSearch]:
        """Search for products by query."""
        pass

    @abstractmethod
    async def get_product_details(self, url: str) -> ProductSearch | None:
        """Get detailed product information from product page."""
        pass

    async def _random_delay(self) -> None:
        """Add random delay to avoid rate limiting."""
        delay = self.rate_limit_delay + random.uniform(0.5, 1.5)
        await asyncio.sleep(delay)

    def _get_random_user_agent(self) -> str:
        """Get a random user agent string."""
        return random.choice(USER_AGENTS)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def _fetch_page(self, page: Page, url: str) -> None:
        """Fetch a page with retry logic."""
        logger.debug(f"Fetching {url}")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await self._random_delay()

    async def _accept_cookies(self, page: Page) -> None:
        """Try to accept cookie consent."""
        selector = self.config["selectors"].get("cookie_accept")
        if selector:
            try:
                button = page.locator(selector)
                if await button.count() > 0:
                    await button.first.click()
                    await asyncio.sleep(1)
                    logger.debug(f"Accepted cookies for {self.supermarket_name}")
            except Exception as e:
                logger.debug(f"Could not accept cookies: {e}")

    async def _create_browser(self) -> tuple[Any, Browser]:
        """Create a new browser instance."""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        return playwright, browser

    async def _create_page(self, browser: Browser) -> Page:
        """Create a new page with stealth settings."""
        context = await browser.new_context(
            user_agent=self._get_random_user_agent(),
            viewport={"width": 1920, "height": 1080},
            locale="nl-NL",
        )
        page = await context.new_page()
        return page

    def _parse_price(self, price_text: str | None) -> float | None:
        """Parse price text to float."""
        if not price_text:
            return None
        # Remove currency symbols and whitespace
        cleaned = re.sub(r"[€\s]", "", price_text)
        # Replace comma with dot for decimal
        cleaned = cleaned.replace(",", ".")
        # Extract numeric value
        match = re.search(r"(\d+\.?\d*)", cleaned)
        if match:
            return float(match.group(1))
        return None

    def _extract_unit_info(self, text: str) -> tuple[str, float]:
        """Extract unit type and size from product text."""
        text_lower = text.lower()

        # Common patterns
        patterns = [
            (r"(\d+(?:[.,]\d+)?)\s*(?:l|liter)", "liter"),
            (r"(\d+(?:[.,]\d+)?)\s*(?:ml)", "ml"),
            (r"(\d+(?:[.,]\d+)?)\s*(?:kg)", "kg"),
            (r"(\d+(?:[.,]\d+)?)\s*(?:g|gram)", "gram"),
            (r"(\d+)\s*(?:st|stuks?)", "stuk"),
        ]

        for pattern, unit in patterns:
            match = re.search(pattern, text_lower)
            if match:
                size = float(match.group(1).replace(",", "."))
                return unit, size

        return "stuk", 1.0
