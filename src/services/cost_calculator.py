"""Cost calculator service for calculating total shopping costs."""

from dataclasses import dataclass
from loguru import logger

from src.models.supermarket import Supermarket
from src.models.shopping_list import ShoppingListComparison
from src.models.product import ProductSearch


@dataclass
class ShoppingItem:
    """Item in shopping list with matched products."""

    product_name: str
    quantity: int
    prices: dict[str, float]  # supermarket -> best price


class CostCalculatorService:
    """Service for calculating shopping costs across supermarkets."""

    def _get_best_price(
        self, product: ProductSearch, has_bonus_card: bool = True
    ) -> float:
        """Get the best available price for a product."""
        prices = [product.regular_price]

        if product.sale_price:
            prices.append(product.sale_price)

        if has_bonus_card and product.bonus_card_price:
            prices.append(product.bonus_card_price)

        return min(prices)

    def calculate_product_total(
        self,
        items: list[dict],
        supermarket_name: str,
        has_bonus_card: bool = True,
    ) -> float:
        """Calculate total cost for products at a supermarket."""
        total = 0.0

        for item in items:
            prices = item.get("prices", {})
            price = prices.get(supermarket_name)

            if price is not None:
                quantity = item.get("quantity", 1)
                total += price * quantity

        return total

    def calculate_delivery_cost(
        self,
        supermarket: Supermarket,
        product_total: float,
        delivery_method: str,
    ) -> float:
        """Calculate delivery/pickup cost."""
        if delivery_method == "pickup":
            if supermarket.pickup_available:
                return supermarket.pickup_cost
            return float("inf")  # Pickup not available

        # Delivery
        if supermarket.free_delivery_threshold:
            if product_total >= supermarket.free_delivery_threshold:
                return 0.0

        return supermarket.delivery_cost

    def calculate_total_cost(
        self,
        items: list[dict],
        supermarket: Supermarket,
        delivery_method: str,
        has_bonus_card: bool = True,
    ) -> ShoppingListComparison:
        """Calculate total shopping cost at a supermarket."""
        product_total = self.calculate_product_total(
            items, supermarket.name, has_bonus_card
        )

        delivery_cost = self.calculate_delivery_cost(
            supermarket, product_total, delivery_method
        )

        total = product_total + delivery_cost

        return ShoppingListComparison(
            supermarket=supermarket.display_name,
            delivery_method=delivery_method,
            product_total=round(product_total, 2),
            delivery_cost=round(delivery_cost, 2),
            total=round(total, 2),
            items=items,
            savings=0.0,  # Will be calculated later
        )

    def compare_all_options(
        self,
        items: list[dict],
        supermarkets: list[Supermarket],
        has_bonus_card: bool = True,
    ) -> list[ShoppingListComparison]:
        """Compare shopping costs across all supermarkets and delivery options."""
        options: list[ShoppingListComparison] = []

        for supermarket in supermarkets:
            # Check delivery option
            delivery_result = self.calculate_total_cost(
                items, supermarket, "delivery", has_bonus_card
            )
            if delivery_result.total < float("inf"):
                options.append(delivery_result)

            # Check pickup option
            if supermarket.pickup_available:
                pickup_result = self.calculate_total_cost(
                    items, supermarket, "pickup", has_bonus_card
                )
                if pickup_result.total < float("inf"):
                    options.append(pickup_result)

        # Sort by total cost
        options.sort(key=lambda x: x.total)

        # Calculate savings compared to most expensive
        if options:
            max_total = max(opt.total for opt in options)
            min_total = options[0].total

            for opt in options:
                opt.savings = round(max_total - opt.total, 2)

            # Mark cheapest option
            if options:
                options[0].is_cheapest = True

        return options

    def get_cheapest_option(
        self,
        items: list[dict],
        supermarkets: list[Supermarket],
        has_bonus_card: bool = True,
    ) -> ShoppingListComparison | None:
        """Get the single cheapest shopping option."""
        options = self.compare_all_options(items, supermarkets, has_bonus_card)
        return options[0] if options else None

    def calculate_item_savings(
        self, item: dict, supermarkets: list[str]
    ) -> dict:
        """Calculate potential savings for a single item."""
        prices = item.get("prices", {})
        valid_prices = {k: v for k, v in prices.items() if v is not None}

        if len(valid_prices) < 2:
            return {"min": 0, "max": 0, "savings": 0}

        min_price = min(valid_prices.values())
        max_price = max(valid_prices.values())

        cheapest_store = min(valid_prices, key=valid_prices.get)

        return {
            "min_price": min_price,
            "max_price": max_price,
            "savings": round(max_price - min_price, 2),
            "cheapest_store": cheapest_store,
        }
