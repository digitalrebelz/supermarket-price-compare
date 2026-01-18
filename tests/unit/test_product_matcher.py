"""Unit tests for ProductMatcherService."""

import pytest
from src.services.product_matcher import ProductMatcherService
from src.models.product import ProductSearch


class TestProductMatcherService:
    """Tests for ProductMatcherService."""

    def test_calculate_similarity_exact_match(self):
        """Test similarity calculation for exact match."""
        matcher = ProductMatcherService()
        score = matcher.calculate_similarity("Melk halfvol", "Melk halfvol")
        assert score == 1.0

    def test_calculate_similarity_partial_match(self):
        """Test similarity calculation for partial match."""
        matcher = ProductMatcherService()
        score = matcher.calculate_similarity("Melk halfvol", "Halfvolle melk")
        assert score > 0.7  # Should be high due to same words

    def test_calculate_similarity_no_match(self):
        """Test similarity calculation for no match."""
        matcher = ProductMatcherService()
        score = matcher.calculate_similarity("Melk", "Brood")
        assert score < 0.5

    def test_find_best_match_with_results(self):
        """Test finding best match with results."""
        matcher = ProductMatcherService()
        products = [
            ProductSearch(
                name="Campina Halfvolle Melk",
                regular_price=1.49,
                url="",
                supermarket="test",
            ),
            ProductSearch(
                name="Albert Heijn Volle Melk",
                regular_price=1.59,
                url="",
                supermarket="test",
            ),
        ]

        match = matcher.find_best_match("halfvolle melk", products)
        assert match is not None
        assert "Halfvolle" in match.name

    def test_find_best_match_no_results(self):
        """Test finding best match with empty list."""
        matcher = ProductMatcherService()
        match = matcher.find_best_match("melk", [])
        assert match is None

    def test_find_best_match_below_threshold(self):
        """Test finding best match below threshold."""
        matcher = ProductMatcherService(similarity_threshold=0.9)
        products = [
            ProductSearch(
                name="Brood volkoren",
                regular_price=2.19,
                url="",
                supermarket="test",
            ),
        ]

        match = matcher.find_best_match("melk", products)
        assert match is None  # No match above 90% threshold

    def test_match_products_across_stores(self, mock_search_results):
        """Test matching products across stores."""
        matcher = ProductMatcherService()
        matches = matcher.match_products_across_stores("melk", mock_search_results)

        assert "albert_heijn" in matches
        assert "jumbo" in matches
        assert matches["albert_heijn"] is not None
        assert matches["jumbo"] is not None

    def test_group_similar_products(self):
        """Test grouping similar products."""
        matcher = ProductMatcherService()
        products = [
            ProductSearch(
                name="Campina Halfvolle Melk 1L",
                regular_price=1.49,
                url="",
                supermarket="ah",
            ),
            ProductSearch(
                name="Campina Halfvolle Melk 1 Liter",
                regular_price=1.59,
                url="",
                supermarket="jumbo",
            ),
            ProductSearch(
                name="Volkoren Brood",
                regular_price=2.19,
                url="",
                supermarket="ah",
            ),
        ]

        groups = matcher.group_similar_products(products)
        assert len(groups) == 2  # Melk group and Brood group

    def test_get_price_comparison(self, mock_search_results):
        """Test getting price comparison."""
        matcher = ProductMatcherService()
        comparison = matcher.get_price_comparison("melk", mock_search_results)

        assert "albert_heijn" in comparison
        assert comparison["albert_heijn"]["regular_price"] == 1.49
        assert comparison["albert_heijn"]["best_price"] == 0.99  # Bonus price
