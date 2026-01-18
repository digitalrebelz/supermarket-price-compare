"""End-to-end tests for Streamlit UI."""

import pytest
from pathlib import Path


# Note: These tests require the Streamlit app to be running
# They are designed to be run with playwright and streamlit test mode


class TestStreamlitApp:
    """E2E tests for Streamlit application."""

    SCREENSHOTS_DIR = Path(__file__).parent.parent / "screenshots"

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment."""
        self.SCREENSHOTS_DIR.mkdir(exist_ok=True)

    def take_screenshot(self, page, name: str):
        """Take a screenshot and save it."""
        path = self.SCREENSHOTS_DIR / f"{name}.png"
        page.screenshot(path=str(path))
        return path

    @pytest.mark.skip(reason="Requires running Streamlit app")
    def test_homepage_loads(self, page):
        """Test that homepage loads correctly."""
        page.goto("http://localhost:8501")
        page.wait_for_load_state("networkidle")

        self.take_screenshot(page, "01_homepage")

        # Check title is present
        assert page.locator("text=Boodschappen Prijsvergelijker").is_visible()

    @pytest.mark.skip(reason="Requires running Streamlit app")
    def test_search_products(self, page):
        """Test product search functionality."""
        page.goto("http://localhost:8501")
        page.wait_for_load_state("networkidle")

        # Enter search query
        search_input = page.locator('input[placeholder="bijv. Melk"]')
        search_input.fill("Melk")

        self.take_screenshot(page, "02_search_input")

        # Click search button
        page.locator('button:has-text("Zoeken")').click()
        page.wait_for_load_state("networkidle")

        self.take_screenshot(page, "03_search_results")

    @pytest.mark.skip(reason="Requires running Streamlit app")
    def test_add_to_shopping_list(self, page):
        """Test adding product to shopping list."""
        page.goto("http://localhost:8501")
        page.wait_for_load_state("networkidle")

        # Search for product
        search_input = page.locator('input[placeholder="bijv. Melk"]')
        search_input.fill("Melk")
        page.locator('button:has-text("Zoeken")').click()
        page.wait_for_load_state("networkidle")

        # Click on search results tab
        page.locator('button:has-text("Zoekresultaten")').click()

        self.take_screenshot(page, "04_search_results_tab")

        # Add first product
        add_buttons = page.locator('button:has-text("➕")')
        if add_buttons.count() > 0:
            add_buttons.first.click()
            page.wait_for_load_state("networkidle")

        self.take_screenshot(page, "05_product_added")

    @pytest.mark.skip(reason="Requires running Streamlit app")
    def test_price_comparison(self, page):
        """Test price comparison functionality."""
        page.goto("http://localhost:8501")
        page.wait_for_load_state("networkidle")

        # Need to have items in shopping list first
        # This test assumes there are items already

        # Click compare button
        compare_button = page.locator('button:has-text("Vergelijk prijzen")')
        if compare_button.is_visible():
            compare_button.click()
            page.wait_for_load_state("networkidle")

            self.take_screenshot(page, "06_comparison_results")

            # Check for comparison results
            assert page.locator("text=Voordeligste").is_visible() or \
                   page.locator("text=Lijst is leeg").is_visible()

    @pytest.mark.skip(reason="Requires running Streamlit app")
    def test_settings_page(self, page):
        """Test settings page."""
        page.goto("http://localhost:8501")
        page.wait_for_load_state("networkidle")

        # Click settings tab
        page.locator('button:has-text("Instellingen")').click()

        self.take_screenshot(page, "07_settings_page")

        # Check for bonus card checkboxes
        assert page.locator("text=Albert Heijn Bonuskaart").is_visible()
        assert page.locator("text=Jumbo Extra").is_visible()

    @pytest.mark.skip(reason="Requires running Streamlit app")
    def test_full_user_flow(self, page):
        """Test complete user flow from search to comparison."""
        # 1. Load homepage
        page.goto("http://localhost:8501")
        page.wait_for_load_state("networkidle")
        self.take_screenshot(page, "flow_01_homepage")

        # 2. Search for product
        search_input = page.locator('input[placeholder="bijv. Melk"]')
        search_input.fill("Brood")
        page.locator('button:has-text("Zoeken")').click()
        page.wait_for_timeout(3000)
        self.take_screenshot(page, "flow_02_search")

        # 3. Go to search results
        page.locator('button:has-text("Zoekresultaten")').click()
        page.wait_for_timeout(1000)
        self.take_screenshot(page, "flow_03_results")

        # 4. Add product
        add_buttons = page.locator('button:has-text("➕")')
        if add_buttons.count() > 0:
            add_buttons.first.click()
            page.wait_for_timeout(1000)
        self.take_screenshot(page, "flow_04_added")

        # 5. Go to comparison
        page.locator('button:has-text("Vergelijking")').click()
        page.wait_for_timeout(1000)
        self.take_screenshot(page, "flow_05_comparison_tab")

        # 6. Compare prices
        compare_button = page.locator('button:has-text("Vergelijk prijzen")')
        if compare_button.is_visible():
            compare_button.click()
            page.wait_for_timeout(5000)
        self.take_screenshot(page, "flow_06_compared")

        # 7. Check settings
        page.locator('button:has-text("Instellingen")').click()
        page.wait_for_timeout(1000)
        self.take_screenshot(page, "flow_07_settings")
