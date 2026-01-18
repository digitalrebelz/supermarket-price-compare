"""Constants for supermarket scraping."""

from typing import TypedDict


class SupermarketConfig(TypedDict):
    """Supermarket configuration type."""

    name: str
    display_name: str
    base_url: str
    search_url: str
    delivery_cost: float
    free_delivery_threshold: float | None
    pickup_available: bool
    pickup_cost: float
    has_bonus_card: bool
    bonus_card_name: str | None
    selectors: dict[str, str]


SUPERMARKETS: dict[str, SupermarketConfig] = {
    "albert_heijn": {
        "name": "albert_heijn",
        "display_name": "Albert Heijn",
        "base_url": "https://www.ah.nl",
        "search_url": "https://www.ah.nl/zoeken?query={query}",
        "delivery_cost": 5.95,
        "free_delivery_threshold": None,
        "pickup_available": True,
        "pickup_cost": 0.0,
        "has_bonus_card": True,
        "bonus_card_name": "Bonuskaart",
        "selectors": {
            "product_card": '[data-testhook="product-card"]',
            "product_title": '[data-testhook="product-title"]',
            "product_price": '[data-testhook="price"]',
            "bonus_price": '[data-testhook="bonus-price"]',
            "cookie_accept": "#accept-cookies",
        },
    },
    "jumbo": {
        "name": "jumbo",
        "display_name": "Jumbo",
        "base_url": "https://www.jumbo.com",
        "search_url": "https://www.jumbo.com/zoeken?searchTerms={query}",
        "delivery_cost": 7.95,
        "free_delivery_threshold": 75.0,
        "pickup_available": True,
        "pickup_cost": 0.0,
        "has_bonus_card": True,
        "bonus_card_name": "Extra's",
        "selectors": {
            "product_card": '[data-testid="product-card"]',
            "product_title": '[data-testid="product-title"]',
            "product_price": '[data-testid="price"]',
            "cookie_accept": "#onetrust-accept-btn-handler",
        },
    },
    "dirk": {
        "name": "dirk",
        "display_name": "Dirk",
        "base_url": "https://www.dirk.nl",
        "search_url": "https://www.dirk.nl/zoeken?q={query}",
        "delivery_cost": 5.95,
        "free_delivery_threshold": None,
        "pickup_available": True,
        "pickup_cost": 0.0,
        "has_bonus_card": False,
        "bonus_card_name": None,
        "selectors": {
            "product_card": ".product-card",
            "product_title": ".product-card__title",
            "product_price": ".product-card__price",
            "cookie_accept": ".cookie-consent__accept",
        },
    },
    "plus": {
        "name": "plus",
        "display_name": "Plus",
        "base_url": "https://www.plus.nl",
        "search_url": "https://www.plus.nl/zoeken?q={query}",
        "delivery_cost": 6.95,
        "free_delivery_threshold": None,
        "pickup_available": True,
        "pickup_cost": 0.0,
        "has_bonus_card": True,
        "bonus_card_name": "Plus-punten",
        "selectors": {
            "product_card": ".product-tile",
            "product_title": ".product-tile__title",
            "product_price": ".product-tile__price",
            "cookie_accept": "#CybotCookiebotDialogBodyButtonAccept",
        },
    },
    "flink": {
        "name": "flink",
        "display_name": "Flink",
        "base_url": "https://www.goflink.com",
        "search_url": "https://www.goflink.com/nl/search?q={query}",
        "delivery_cost": 2.99,
        "free_delivery_threshold": None,
        "pickup_available": False,
        "pickup_cost": 0.0,
        "has_bonus_card": False,
        "bonus_card_name": None,
        "selectors": {
            "product_card": "[data-testid='product-card']",
            "product_title": "[data-testid='product-name']",
            "product_price": "[data-testid='product-price']",
            "cookie_accept": "[data-testid='cookie-accept']",
        },
    },
    "picnic": {
        "name": "picnic",
        "display_name": "Picnic",
        "base_url": "https://picnic.app",
        "search_url": "https://picnic.app/nl/search/{query}",
        "delivery_cost": 0.0,
        "free_delivery_threshold": 35.0,
        "pickup_available": False,
        "pickup_cost": 0.0,
        "has_bonus_card": False,
        "bonus_card_name": None,
        "selectors": {
            "product_card": ".product-card",
            "product_title": ".product-card__name",
            "product_price": ".product-card__price",
            "cookie_accept": ".cookie-banner__accept",
        },
    },
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/17.2",
]
