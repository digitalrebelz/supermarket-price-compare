"""Unit tests for CostCalculatorService."""

import pytest
from src.services.cost_calculator import CostCalculatorService
from src.models.supermarket import Supermarket


@pytest.fixture
def calculator():
    """Create a CostCalculatorService instance."""
    return CostCalculatorService()


@pytest.fixture
def supermarkets():
    """Create sample supermarkets for testing."""
    return [
        Supermarket(
            id=1,
            name="albert_heijn",
            display_name="Albert Heijn",
            base_url="https://www.ah.nl",
            delivery_cost=5.95,
            free_delivery_threshold=None,
            pickup_available=True,
            pickup_cost=0.0,
            has_bonus_card=True,
            bonus_card_name="Bonuskaart",
        ),
        Supermarket(
            id=2,
            name="jumbo",
            display_name="Jumbo",
            base_url="https://www.jumbo.com",
            delivery_cost=7.95,
            free_delivery_threshold=75.0,
            pickup_available=True,
            pickup_cost=0.0,
            has_bonus_card=True,
            bonus_card_name="Extra's",
        ),
        Supermarket(
            id=3,
            name="picnic",
            display_name="Picnic",
            base_url="https://picnic.app",
            delivery_cost=0.0,
            free_delivery_threshold=35.0,
            pickup_available=False,
            pickup_cost=0.0,
            has_bonus_card=False,
            bonus_card_name=None,
        ),
    ]


class TestCostCalculatorService:
    """Tests for CostCalculatorService."""

    def test_calculate_product_total(self, calculator, sample_shopping_list):
        """Test calculating product total."""
        total = calculator.calculate_product_total(
            sample_shopping_list, "albert_heijn"
        )
        # 2 * 1.49 + 1 * 2.19 + 1 * 4.99 = 10.16
        assert total == pytest.approx(10.16, 0.01)

    def test_calculate_delivery_cost_no_free_threshold(self, calculator, supermarkets):
        """Test delivery cost without free threshold."""
        ah = supermarkets[0]  # Albert Heijn
        cost = calculator.calculate_delivery_cost(ah, 50.0, "delivery")
        assert cost == 5.95

    def test_calculate_delivery_cost_with_free_threshold_below(
        self, calculator, supermarkets
    ):
        """Test delivery cost with free threshold (below)."""
        jumbo = supermarkets[1]
        cost = calculator.calculate_delivery_cost(jumbo, 50.0, "delivery")
        assert cost == 7.95  # Below €75 threshold

    def test_calculate_delivery_cost_with_free_threshold_above(
        self, calculator, supermarkets
    ):
        """Test delivery cost with free threshold (above)."""
        jumbo = supermarkets[1]
        cost = calculator.calculate_delivery_cost(jumbo, 100.0, "delivery")
        assert cost == 0.0  # Above €75 threshold

    def test_calculate_delivery_cost_pickup(self, calculator, supermarkets):
        """Test pickup cost."""
        ah = supermarkets[0]
        cost = calculator.calculate_delivery_cost(ah, 50.0, "pickup")
        assert cost == 0.0

    def test_calculate_delivery_cost_pickup_not_available(
        self, calculator, supermarkets
    ):
        """Test pickup cost when not available."""
        picnic = supermarkets[2]
        cost = calculator.calculate_delivery_cost(picnic, 50.0, "pickup")
        assert cost == float("inf")

    def test_calculate_total_cost(
        self, calculator, sample_shopping_list, supermarkets
    ):
        """Test calculating total cost."""
        ah = supermarkets[0]
        result = calculator.calculate_total_cost(
            sample_shopping_list, ah, "delivery"
        )

        assert result.supermarket == "Albert Heijn"
        assert result.delivery_method == "delivery"
        assert result.product_total == pytest.approx(10.16, 0.01)
        assert result.delivery_cost == 5.95
        assert result.total == pytest.approx(16.11, 0.01)

    def test_compare_all_options(
        self, calculator, sample_shopping_list, supermarkets
    ):
        """Test comparing all options."""
        options = calculator.compare_all_options(
            sample_shopping_list, supermarkets
        )

        # Should have multiple options
        assert len(options) >= 3

        # Should be sorted by total cost
        for i in range(len(options) - 1):
            assert options[i].total <= options[i + 1].total

        # First option should be marked as cheapest
        assert options[0].is_cheapest

        # Should have calculated savings
        assert options[0].savings >= 0

    def test_calculate_item_savings(self, calculator):
        """Test calculating item savings."""
        item = {
            "product_name": "Melk",
            "quantity": 1,
            "prices": {"albert_heijn": 1.49, "jumbo": 1.59, "dirk": 1.39},
        }

        savings = calculator.calculate_item_savings(
            item, ["albert_heijn", "jumbo", "dirk"]
        )

        assert savings["min_price"] == 1.39
        assert savings["max_price"] == 1.59
        assert savings["savings"] == 0.20
        assert savings["cheapest_store"] == "dirk"
