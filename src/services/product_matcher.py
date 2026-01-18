"""Product matcher service for matching products across supermarkets."""

from fuzzywuzzy import fuzz
from loguru import logger

from src.models.product import ProductSearch


class ProductMatcherService:
    """Service for matching similar products across supermarkets."""

    def __init__(self, similarity_threshold: float = 0.7):
        """Initialize product matcher."""
        self.similarity_threshold = similarity_threshold

    def calculate_similarity(self, product1: str, product2: str) -> float:
        """Calculate similarity score between two product names."""
        # Use token sort ratio for better matching of rearranged words
        score = fuzz.token_sort_ratio(product1.lower(), product2.lower())
        return score / 100.0

    def find_best_match(
        self, query: str, products: list[ProductSearch]
    ) -> ProductSearch | None:
        """Find the best matching product for a query."""
        if not products:
            return None

        best_match = None
        best_score = 0.0

        for product in products:
            score = self.calculate_similarity(query, product.name)
            if score > best_score:
                best_score = score
                best_match = product

        if best_score >= self.similarity_threshold:
            return best_match
        return None

    def match_products_across_stores(
        self, query: str, results: dict[str, list[ProductSearch]]
    ) -> dict[str, ProductSearch | None]:
        """Find best matching product in each supermarket."""
        matches: dict[str, ProductSearch | None] = {}

        for supermarket, products in results.items():
            match = self.find_best_match(query, products)
            matches[supermarket] = match

            if match:
                logger.debug(
                    f"{supermarket}: matched '{query}' -> '{match.name}'"
                )

        return matches

    def group_similar_products(
        self, products: list[ProductSearch]
    ) -> list[list[ProductSearch]]:
        """Group similar products together."""
        if not products:
            return []

        groups: list[list[ProductSearch]] = []
        used_indices: set[int] = set()

        for i, product in enumerate(products):
            if i in used_indices:
                continue

            # Start a new group
            group = [product]
            used_indices.add(i)

            # Find similar products
            for j, other in enumerate(products):
                if j in used_indices:
                    continue

                similarity = self.calculate_similarity(product.name, other.name)
                if similarity >= self.similarity_threshold:
                    group.append(other)
                    used_indices.add(j)

            groups.append(group)

        return groups

    def find_exact_match(
        self, name: str, brand: str | None, products: list[ProductSearch]
    ) -> ProductSearch | None:
        """Find exact product match by name and brand."""
        for product in products:
            name_match = product.name.lower() == name.lower()
            brand_match = (
                not brand
                or not product.brand
                or product.brand.lower() == brand.lower()
            )

            if name_match and brand_match:
                return product

        return None

    def get_price_comparison(
        self, query: str, results: dict[str, list[ProductSearch]]
    ) -> dict[str, dict]:
        """Get price comparison for a product across all supermarkets."""
        matches = self.match_products_across_stores(query, results)

        comparison = {}
        for supermarket, match in matches.items():
            if match:
                comparison[supermarket] = {
                    "name": match.name,
                    "regular_price": match.regular_price,
                    "sale_price": match.sale_price,
                    "bonus_card_price": match.bonus_card_price,
                    "best_price": match.bonus_card_price
                    or match.sale_price
                    or match.regular_price,
                    "url": match.url,
                }
            else:
                comparison[supermarket] = None

        return comparison
