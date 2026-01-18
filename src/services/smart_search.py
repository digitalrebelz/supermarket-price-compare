"""Smart search service that finds both branded and house brand products."""

from loguru import logger
from src.models.product import ProductSearch
from src.scrapers.ah_api import AlbertHeijnAPIScraper
from src.services.mock_data import MOCK_PRODUCTS

# Mapping of generic product names to search variations
PRODUCT_VARIATIONS = {
    "cola": ["cola", "ah cola", "coca cola", "pepsi"],
    "melk": ["melk", "ah melk", "campina melk", "halfvolle melk"],
    "brood": ["brood", "ah brood", "heel brood", "volkoren brood"],
    "kaas": ["kaas", "ah kaas", "goudse kaas", "jong belegen"],
    "eieren": ["eieren", "ah eieren", "scharreleieren", "vrije uitloop"],
    "bier": ["bier", "heineken", "amstel", "ah bier", "pilsener"],
    "chips": ["chips", "ah chips", "lays", "doritos"],
    "pasta": ["pasta", "spaghetti", "ah pasta", "penne"],
    "koffie": ["koffie", "ah koffie", "douwe egberts", "nespresso"],
    "thee": ["thee", "ah thee", "pickwick", "lipton"],
    "yoghurt": ["yoghurt", "ah yoghurt", "activia", "danone"],
    "boter": ["boter", "ah boter", "roomboter", "margarine"],
}

# House brand names per supermarket
HOUSE_BRANDS = {
    "albert_heijn": ["AH", "AH Excellent", "AH Basic", "AH Biologisch"],
    "jumbo": ["Jumbo", "Jumbo Biologisch"],
    "dirk": ["Dirk", "River"],
    "plus": ["Plus", "PLUS"],
    "flink": [],
    "picnic": ["Picnic"],
}


def get_search_variations(query: str) -> list[str]:
    """Get search variations for a query to include house brands."""
    query_lower = query.lower().strip()

    # Check if we have predefined variations
    for key, variations in PRODUCT_VARIATIONS.items():
        if key in query_lower or query_lower in key:
            return variations

    # Default: search original + "ah" prefix for house brand
    return [query_lower, f"ah {query_lower}"]


def smart_search(query: str) -> dict[str, list[ProductSearch]]:
    """
    Smart search that finds both branded and house brand products.
    Returns results grouped by supermarket with cheapest options highlighted.
    """
    all_results: dict[str, list[ProductSearch]] = {
        "albert_heijn": [],
        "jumbo": [],
        "dirk": [],
        "plus": [],
        "flink": [],
        "picnic": [],
    }

    seen_products: dict[str, set] = {store: set() for store in all_results}

    # Get search variations
    variations = get_search_variations(query)
    logger.info(f"Smart search for '{query}' with variations: {variations}")

    # Search AH API with all variations
    try:
        ah_scraper = AlbertHeijnAPIScraper()
        for variation in variations:
            try:
                results = ah_scraper.search_product(variation, limit=10)
                for product in results:
                    # Avoid duplicates
                    product_key = f"{product.name}_{product.regular_price}"
                    if product_key not in seen_products["albert_heijn"]:
                        seen_products["albert_heijn"].add(product_key)
                        all_results["albert_heijn"].append(product)
            except Exception as e:
                logger.debug(f"AH search for '{variation}' failed: {e}")
    except Exception as e:
        logger.error(f"AH API not available: {e}")

    # Add mock data for other supermarkets
    query_lower = query.lower().strip()
    for keyword, products in MOCK_PRODUCTS.items():
        # Check if query matches this category
        if keyword in query_lower or query_lower in keyword:
            for product in products:
                store = product["store"]
                # Skip AH if we already have real data
                if store == "albert_heijn" and all_results["albert_heijn"]:
                    continue

                product_key = f"{product['name']}_{product['regular']}"
                if product_key not in seen_products[store]:
                    seen_products[store].add(product_key)
                    all_results[store].append(
                        ProductSearch(
                            name=product["name"],
                            brand=product.get("brand"),
                            regular_price=product["regular"],
                            bonus_card_price=product.get("bonus"),
                            url=f"https://www.{store.replace('_', '')}.nl/product",
                            supermarket=store,
                        )
                    )

    # Sort each store's results by price (cheapest first)
    for store in all_results:
        all_results[store].sort(
            key=lambda p: p.bonus_card_price or p.regular_price
        )

    # Log results
    total = sum(len(v) for v in all_results.values())
    logger.info(f"Smart search found {total} products for '{query}'")

    return all_results


def get_cheapest_per_store(results: dict[str, list[ProductSearch]]) -> dict[str, ProductSearch | None]:
    """Get the cheapest product per store."""
    cheapest = {}
    for store, products in results.items():
        if products:
            # Already sorted by price
            cheapest[store] = products[0]
        else:
            cheapest[store] = None
    return cheapest


def calculate_basket_comparison(
    shopping_list: list[dict],
    include_delivery: bool = True
) -> list[dict]:
    """
    Calculate total cost per supermarket for a shopping list.

    Args:
        shopping_list: List of items with product_name and quantity
        include_delivery: Whether to include delivery costs

    Returns:
        List of supermarket options sorted by total cost
    """
    from src.config.constants import SUPERMARKETS

    # Initialize totals per supermarket
    store_totals = {
        store: {"products": 0, "items_found": 0, "items_missing": 0, "details": []}
        for store in SUPERMARKETS
    }

    # For each item in shopping list, find cheapest option per store
    for item in shopping_list:
        query = item.get("product_name", item.get("name", ""))
        quantity = item.get("quantity", 1)

        # Search for this product
        results = smart_search(query)
        cheapest = get_cheapest_per_store(results)

        for store, product in cheapest.items():
            if product:
                price = product.bonus_card_price or product.regular_price
                store_totals[store]["products"] += price * quantity
                store_totals[store]["items_found"] += 1
                store_totals[store]["details"].append({
                    "query": query,
                    "product": product.name,
                    "price": price,
                    "quantity": quantity,
                })
            else:
                store_totals[store]["items_missing"] += 1

    # Build comparison list
    comparison = []
    for store, data in store_totals.items():
        config = SUPERMARKETS[store]

        delivery_cost = 0
        if include_delivery:
            threshold = config.get("free_delivery_threshold")
            if threshold and data["products"] >= threshold:
                delivery_cost = 0
            else:
                delivery_cost = config.get("delivery_cost", 0)

        total = data["products"] + delivery_cost

        comparison.append({
            "supermarket": config["display_name"],
            "store_key": store,
            "product_total": round(data["products"], 2),
            "delivery_cost": round(delivery_cost, 2),
            "total": round(total, 2),
            "items_found": data["items_found"],
            "items_missing": data["items_missing"],
            "details": data["details"],
        })

    # Sort by total cost
    comparison.sort(key=lambda x: (x["items_missing"], x["total"]))

    # Mark cheapest
    if comparison:
        comparison[0]["is_cheapest"] = True

    return comparison
