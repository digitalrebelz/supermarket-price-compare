"""Mock data for demo mode when scrapers are blocked."""

from src.models.product import ProductSearch

# Realistic Dutch supermarket product data
MOCK_PRODUCTS: dict[str, list[dict]] = {
    "cola": [
        {"name": "Coca-Cola Regular 1.5L", "brand": "Coca-Cola", "regular": 2.29, "bonus": 1.79, "store": "albert_heijn"},
        {"name": "Coca-Cola Zero 1.5L", "brand": "Coca-Cola", "regular": 2.29, "bonus": 1.79, "store": "albert_heijn"},
        {"name": "Pepsi Cola Regular 1.5L", "brand": "Pepsi", "regular": 1.99, "bonus": None, "store": "albert_heijn"},
        {"name": "Coca-Cola Original Taste 1.5L", "brand": "Coca-Cola", "regular": 2.39, "bonus": None, "store": "jumbo"},
        {"name": "Coca-Cola Zero Sugar 1.5L", "brand": "Coca-Cola", "regular": 2.39, "bonus": 1.89, "store": "jumbo"},
        {"name": "Pepsi Max 1.5L", "brand": "Pepsi", "regular": 1.89, "bonus": None, "store": "jumbo"},
        {"name": "Coca-Cola Regular 1.5L", "brand": "Coca-Cola", "regular": 2.19, "bonus": None, "store": "dirk"},
        {"name": "River Cola 1.5L", "brand": "River", "regular": 0.69, "bonus": None, "store": "dirk"},
        {"name": "Coca-Cola Original 1.5L", "brand": "Coca-Cola", "regular": 2.35, "bonus": 1.99, "store": "plus"},
        {"name": "Coca-Cola 1.5L", "brand": "Coca-Cola", "regular": 2.49, "bonus": None, "store": "flink"},
        {"name": "Coca-Cola Regular 1.5L", "brand": "Coca-Cola", "regular": 2.19, "bonus": None, "store": "picnic"},
    ],
    "melk": [
        {"name": "Campina Halfvolle Melk 1L", "brand": "Campina", "regular": 1.39, "bonus": 0.99, "store": "albert_heijn"},
        {"name": "AH Halfvolle Melk 1L", "brand": "AH", "regular": 1.15, "bonus": None, "store": "albert_heijn"},
        {"name": "Campina Volle Melk 1L", "brand": "Campina", "regular": 1.45, "bonus": None, "store": "albert_heijn"},
        {"name": "Campina Halfvolle Melk 1L", "brand": "Campina", "regular": 1.45, "bonus": 1.09, "store": "jumbo"},
        {"name": "Jumbo Halfvolle Melk 1L", "brand": "Jumbo", "regular": 1.09, "bonus": None, "store": "jumbo"},
        {"name": "Campina Halfvolle Melk 1L", "brand": "Campina", "regular": 1.35, "bonus": None, "store": "dirk"},
        {"name": "Dirk Halfvolle Melk 1L", "brand": "Dirk", "regular": 0.99, "bonus": None, "store": "dirk"},
        {"name": "Campina Halfvolle Melk 1L", "brand": "Campina", "regular": 1.42, "bonus": 1.19, "store": "plus"},
        {"name": "Campina Halfvolle Melk 1L", "brand": "Campina", "regular": 1.49, "bonus": None, "store": "flink"},
        {"name": "Campina Halfvolle Melk 1L", "brand": "Campina", "regular": 1.35, "bonus": None, "store": "picnic"},
    ],
    "brood": [
        {"name": "Heel Bruin Brood", "brand": "AH", "regular": 1.89, "bonus": 1.49, "store": "albert_heijn"},
        {"name": "Tijgerbrood Wit", "brand": "AH", "regular": 2.29, "bonus": None, "store": "albert_heijn"},
        {"name": "Boeren Wit Brood", "brand": "Jumbo", "regular": 1.99, "bonus": None, "store": "jumbo"},
        {"name": "Heel Bruin Brood", "brand": "Jumbo", "regular": 1.79, "bonus": 1.39, "store": "jumbo"},
        {"name": "Bruin Brood Heel", "brand": "Dirk", "regular": 1.49, "bonus": None, "store": "dirk"},
        {"name": "Wit Brood Heel", "brand": "Dirk", "regular": 1.39, "bonus": None, "store": "dirk"},
        {"name": "Boeren Bruin Brood", "brand": "Plus", "regular": 1.89, "bonus": 1.59, "store": "plus"},
        {"name": "Bruin Brood", "brand": "Flink", "regular": 2.19, "bonus": None, "store": "flink"},
        {"name": "Heel Bruin Brood", "brand": "Picnic", "regular": 1.69, "bonus": None, "store": "picnic"},
    ],
    "kaas": [
        {"name": "Goudse Kaas Jong 48+ 400g", "brand": "AH", "regular": 4.99, "bonus": 3.99, "store": "albert_heijn"},
        {"name": "Old Amsterdam 250g", "brand": "Old Amsterdam", "regular": 5.49, "bonus": 4.49, "store": "albert_heijn"},
        {"name": "Goudse Jong 48+ 400g", "brand": "Jumbo", "regular": 4.79, "bonus": 3.79, "store": "jumbo"},
        {"name": "Goudse Kaas Jong 400g", "brand": "Dirk", "regular": 4.29, "bonus": None, "store": "dirk"},
        {"name": "Goudse Kaas Jong Belegen 400g", "brand": "Plus", "regular": 4.89, "bonus": 3.99, "store": "plus"},
        {"name": "Goudse Kaas Jong 400g", "brand": "Flink", "regular": 5.29, "bonus": None, "store": "flink"},
        {"name": "Goudse Jong 48+ 400g", "brand": "Picnic", "regular": 4.49, "bonus": None, "store": "picnic"},
    ],
    "eieren": [
        {"name": "Scharreleieren 10 stuks", "brand": "AH", "regular": 3.29, "bonus": 2.49, "store": "albert_heijn"},
        {"name": "Vrije Uitloop Eieren 10 stuks", "brand": "AH", "regular": 3.99, "bonus": None, "store": "albert_heijn"},
        {"name": "Scharrel Eieren 10 stuks", "brand": "Jumbo", "regular": 3.19, "bonus": 2.39, "store": "jumbo"},
        {"name": "Scharreleieren 10 stuks", "brand": "Dirk", "regular": 2.89, "bonus": None, "store": "dirk"},
        {"name": "Scharrel Eieren 10 stuks", "brand": "Plus", "regular": 3.15, "bonus": 2.69, "store": "plus"},
        {"name": "Scharreleieren 10 stuks", "brand": "Flink", "regular": 3.49, "bonus": None, "store": "flink"},
        {"name": "Scharreleieren 10 stuks", "brand": "Picnic", "regular": 2.99, "bonus": None, "store": "picnic"},
    ],
    "bier": [
        {"name": "Heineken Pilsener 6x33cl", "brand": "Heineken", "regular": 6.99, "bonus": 5.49, "store": "albert_heijn"},
        {"name": "Hertog Jan 6x30cl", "brand": "Hertog Jan", "regular": 6.49, "bonus": None, "store": "albert_heijn"},
        {"name": "Heineken 6x33cl", "brand": "Heineken", "regular": 7.19, "bonus": 5.69, "store": "jumbo"},
        {"name": "Amstel Pilsener 6x33cl", "brand": "Amstel", "regular": 5.99, "bonus": None, "store": "jumbo"},
        {"name": "Heineken 6x33cl", "brand": "Heineken", "regular": 6.79, "bonus": None, "store": "dirk"},
        {"name": "Heineken Pilsener 6x33cl", "brand": "Heineken", "regular": 6.99, "bonus": 5.79, "store": "plus"},
        {"name": "Heineken 6x33cl", "brand": "Heineken", "regular": 7.49, "bonus": None, "store": "flink"},
        {"name": "Heineken 6x33cl", "brand": "Heineken", "regular": 6.69, "bonus": None, "store": "picnic"},
    ],
    "chips": [
        {"name": "Lay's Naturel 225g", "brand": "Lay's", "regular": 2.89, "bonus": 1.99, "store": "albert_heijn"},
        {"name": "Doritos Nacho Cheese 185g", "brand": "Doritos", "regular": 2.99, "bonus": None, "store": "albert_heijn"},
        {"name": "Lay's Naturel 225g", "brand": "Lay's", "regular": 2.79, "bonus": 1.89, "store": "jumbo"},
        {"name": "Lay's Naturel 225g", "brand": "Lay's", "regular": 2.49, "bonus": None, "store": "dirk"},
        {"name": "Lay's Naturel 225g", "brand": "Lay's", "regular": 2.85, "bonus": 2.19, "store": "plus"},
        {"name": "Lay's Naturel 225g", "brand": "Lay's", "regular": 3.19, "bonus": None, "store": "flink"},
        {"name": "Lay's Naturel 225g", "brand": "Lay's", "regular": 2.59, "bonus": None, "store": "picnic"},
    ],
    "pasta": [
        {"name": "De Cecco Spaghetti 500g", "brand": "De Cecco", "regular": 2.49, "bonus": 1.79, "store": "albert_heijn"},
        {"name": "Barilla Penne 500g", "brand": "Barilla", "regular": 1.99, "bonus": None, "store": "albert_heijn"},
        {"name": "De Cecco Spaghetti 500g", "brand": "De Cecco", "regular": 2.59, "bonus": 1.89, "store": "jumbo"},
        {"name": "Barilla Spaghetti 500g", "brand": "Barilla", "regular": 1.79, "bonus": None, "store": "dirk"},
        {"name": "De Cecco Spaghetti 500g", "brand": "De Cecco", "regular": 2.55, "bonus": 1.99, "store": "plus"},
        {"name": "Barilla Spaghetti 500g", "brand": "Barilla", "regular": 2.29, "bonus": None, "store": "flink"},
        {"name": "De Cecco Spaghetti 500g", "brand": "De Cecco", "regular": 2.39, "bonus": None, "store": "picnic"},
    ],
}


def get_mock_results(query: str) -> dict[str, list[ProductSearch]]:
    """Get mock search results for a query."""
    query_lower = query.lower().strip()

    # Find matching products
    matching_products = []
    for keyword, products in MOCK_PRODUCTS.items():
        if keyword in query_lower or query_lower in keyword:
            matching_products.extend(products)

    # If no exact match, return partial matches
    if not matching_products:
        for keyword, products in MOCK_PRODUCTS.items():
            for product in products:
                if query_lower in product["name"].lower():
                    matching_products.append(product)

    # Group by supermarket
    results: dict[str, list[ProductSearch]] = {
        "albert_heijn": [],
        "jumbo": [],
        "dirk": [],
        "plus": [],
        "flink": [],
        "picnic": [],
    }

    for product in matching_products:
        store = product["store"]
        results[store].append(
            ProductSearch(
                name=product["name"],
                brand=product.get("brand"),
                regular_price=product["regular"],
                bonus_card_price=product.get("bonus"),
                url=f"https://www.{store.replace('_', '')}.nl/product/{product['name'].lower().replace(' ', '-')}",
                supermarket=store,
            )
        )

    return results
