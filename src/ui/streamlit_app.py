"""Streamlit UI for Supermarket Price Compare."""

import asyncio
import streamlit as st
import pandas as pd
import plotly.express as px
from loguru import logger

# Add project root to path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.services.scraper_service import ScraperService
from src.services.product_matcher import ProductMatcherService
from src.services.cost_calculator import CostCalculatorService
from src.services.mock_data import get_mock_results
from src.database import get_db
from src.database.crud import get_all_supermarkets, upsert_supermarket
from src.config.constants import SUPERMARKETS
from src.models.supermarket import Supermarket

# Use mock data (real scrapers are blocked by supermarket websites)
USE_MOCK_DATA = True

# Page config
st.set_page_config(
    page_title="Boodschappen Prijsvergelijker",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .price-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background: #f0f2f6;
        margin: 0.5rem 0;
    }
    .cheapest {
        background: #d4edda;
        border: 2px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "shopping_list" not in st.session_state:
        st.session_state.shopping_list = []
    if "search_results" not in st.session_state:
        st.session_state.search_results = {}
    if "comparison_results" not in st.session_state:
        st.session_state.comparison_results = []
    if "settings" not in st.session_state:
        st.session_state.settings = {
            "has_ah_bonus": True,
            "has_jumbo_extras": True,
            "has_plus_points": False,
            "delivery_preference": "Goedkoopste optie",
        }


def init_database():
    """Initialize database with supermarket data."""
    db_manager = get_db()
    with db_manager.get_session() as session:
        for name, config in SUPERMARKETS.items():
            upsert_supermarket(
                session,
                name=config["name"],
                display_name=config["display_name"],
                base_url=config["base_url"],
                delivery_cost=config["delivery_cost"],
                free_delivery_threshold=config["free_delivery_threshold"],
                pickup_available=config["pickup_available"],
                pickup_cost=config["pickup_cost"],
                has_bonus_card=config["has_bonus_card"],
                bonus_card_name=config["bonus_card_name"],
            )


def get_supermarkets_list() -> list[Supermarket]:
    """Get list of supermarkets from database."""
    db_manager = get_db()
    with db_manager.get_session() as session:
        supermarkets_db = get_all_supermarkets(session)
        return [
            Supermarket(
                id=s.id,
                name=s.name,
                display_name=s.display_name,
                base_url=s.base_url,
                delivery_cost=s.delivery_cost,
                free_delivery_threshold=s.free_delivery_threshold,
                pickup_available=s.pickup_available,
                pickup_cost=s.pickup_cost,
                has_bonus_card=s.has_bonus_card,
                bonus_card_name=s.bonus_card_name,
            )
            for s in supermarkets_db
        ]


async def search_products(query: str) -> dict:
    """Search products in all supermarkets."""
    if USE_MOCK_DATA:
        # Use mock data (real websites block scrapers)
        return get_mock_results(query)
    else:
        service = ScraperService()
        results = await service.search_all_supermarkets(query)
        return results


def add_to_shopping_list(product_name: str, prices: dict):
    """Add product to shopping list."""
    # Check if already in list
    for item in st.session_state.shopping_list:
        if item["product_name"].lower() == product_name.lower():
            item["quantity"] += 1
            return

    st.session_state.shopping_list.append({
        "product_name": product_name,
        "quantity": 1,
        "prices": prices,
    })


def remove_from_shopping_list(index: int):
    """Remove product from shopping list."""
    if 0 <= index < len(st.session_state.shopping_list):
        st.session_state.shopping_list.pop(index)


def calculate_comparison():
    """Calculate price comparison for shopping list."""
    if not st.session_state.shopping_list:
        return

    supermarkets = get_supermarkets_list()
    calculator = CostCalculatorService()

    has_bonus = st.session_state.settings.get("has_ah_bonus", True)

    options = calculator.compare_all_options(
        st.session_state.shopping_list,
        supermarkets,
        has_bonus,
    )

    st.session_state.comparison_results = options


# Initialize
init_session_state()
init_database()

# Sidebar
with st.sidebar:
    st.header("🛒 Mijn Boodschappenlijst")

    # Add product
    st.subheader("Product toevoegen")
    search_query = st.text_input("Zoek product", placeholder="bijv. Melk")

    if st.button("🔍 Zoeken", type="primary") and search_query:
        with st.spinner("Zoeken in supermarkten..."):
            try:
                results = asyncio.run(search_products(search_query))
                st.session_state.search_results = results
            except Exception as e:
                st.error(f"Zoeken mislukt: {e}")

    # Shopping list
    st.subheader("Huidige lijst")
    if not st.session_state.shopping_list:
        st.info("Lijst is leeg. Voeg producten toe!")
    else:
        for i, item in enumerate(st.session_state.shopping_list):
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{item['product_name']}**")
            new_qty = col2.number_input(
                "Aantal",
                value=item["quantity"],
                min_value=1,
                key=f"qty_{i}",
                label_visibility="collapsed",
            )
            item["quantity"] = new_qty
            if col3.button("❌", key=f"del_{i}"):
                remove_from_shopping_list(i)
                st.rerun()

        if st.button("🗑️ Lijst wissen"):
            st.session_state.shopping_list = []
            st.session_state.comparison_results = []
            st.rerun()

# Main content
st.title("🛒 Boodschappen Prijsvergelijker")
st.markdown("*Vind de voordeligste supermarkt voor jouw boodschappen*")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Vergelijking", "🔍 Zoekresultaten", "⚙️ Instellingen"])

with tab1:
    st.header("Prijsvergelijking")

    if st.session_state.shopping_list:
        if st.button("🔄 Vergelijk prijzen", type="primary"):
            with st.spinner("Prijzen vergelijken..."):
                calculate_comparison()

        if st.session_state.comparison_results:
            results = st.session_state.comparison_results

            # Best option
            if results:
                best = results[0]
                st.success(
                    f"🏆 **Voordeligste optie:** {best.supermarket} "
                    f"({best.delivery_method}) - **€{best.total:.2f}**"
                )

                if best.savings > 0:
                    st.info(f"💰 Je bespaart tot €{best.savings:.2f}!")

            # Comparison table
            st.subheader("Alle opties")
            df_data = []
            for opt in results:
                df_data.append({
                    "Supermarkt": opt.supermarket,
                    "Methode": "🚚 Bezorgen" if opt.delivery_method == "delivery" else "🏪 Ophalen",
                    "Producten": f"€{opt.product_total:.2f}",
                    "Bezorging": f"€{opt.delivery_cost:.2f}",
                    "Totaal": f"€{opt.total:.2f}",
                    "Besparing": f"€{opt.savings:.2f}",
                })

            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Chart
            st.subheader("Grafiek")
            chart_data = pd.DataFrame([
                {
                    "Optie": f"{opt.supermarket} ({opt.delivery_method})",
                    "Producten": opt.product_total,
                    "Bezorging": opt.delivery_cost,
                }
                for opt in results
            ])

            fig = px.bar(
                chart_data,
                x="Optie",
                y=["Producten", "Bezorging"],
                title="Kosten per supermarkt",
                barmode="stack",
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👈 Voeg producten toe aan je boodschappenlijst om te vergelijken")

with tab2:
    st.header("Zoekresultaten")

    if st.session_state.search_results:
        matcher = ProductMatcherService()

        for supermarket, products in st.session_state.search_results.items():
            display_name = SUPERMARKETS.get(supermarket, {}).get("display_name", supermarket)

            with st.expander(f"🏪 {display_name} ({len(products)} resultaten)"):
                if not products:
                    st.write("Geen producten gevonden")
                    continue

                for idx, product in enumerate(products[:5]):
                    col1, col2, col3 = st.columns([4, 2, 1])

                    col1.write(f"**{product.name}**")

                    # Show prices
                    price_text = f"€{product.regular_price:.2f}"
                    if product.bonus_card_price:
                        price_text += f" (Bonus: €{product.bonus_card_price:.2f})"
                    col2.write(price_text)

                    # Add button with unique key using index
                    if col3.button("➕", key=f"add_{supermarket}_{idx}"):
                        prices = {supermarket: product.bonus_card_price or product.regular_price}
                        add_to_shopping_list(product.name, prices)
                        st.success(f"Toegevoegd: {product.name}")
                        st.rerun()
    else:
        st.info("🔍 Zoek naar producten in de sidebar")

with tab3:
    st.header("Instellingen")

    st.subheader("Bonuskaarten")
    col1, col2 = st.columns(2)

    st.session_state.settings["has_ah_bonus"] = col1.checkbox(
        "Albert Heijn Bonuskaart",
        value=st.session_state.settings.get("has_ah_bonus", True),
    )
    st.session_state.settings["has_jumbo_extras"] = col1.checkbox(
        "Jumbo Extra's",
        value=st.session_state.settings.get("has_jumbo_extras", True),
    )
    st.session_state.settings["has_plus_points"] = col2.checkbox(
        "Plus puntenkaart",
        value=st.session_state.settings.get("has_plus_points", False),
    )

    st.subheader("Bezorgvoorkeur")
    st.session_state.settings["delivery_preference"] = st.radio(
        "Voorkeur",
        ["Goedkoopste optie", "Alleen bezorgen", "Alleen ophalen"],
        index=0,
    )

    st.subheader("Supermarkten")
    st.markdown("""
    | Supermarkt | Bezorging | Gratis vanaf | Ophalen |
    |------------|-----------|--------------|---------|
    | Albert Heijn | €5.95 | - | ✅ |
    | Jumbo | €7.95 | €75 | ✅ |
    | Dirk | €5.95 | - | ✅ |
    | Plus | €6.95 | - | ✅ |
    | Flink | €2.99 | - | ❌ |
    | Picnic | €0 | €35 | ❌ |
    """)

# Debug mode
if st.query_params.get("debug") == "true":
    st.divider()
    st.subheader("🔧 Debug Info")
    st.json({
        "shopping_list": st.session_state.shopping_list,
        "search_results_keys": list(st.session_state.search_results.keys()),
        "comparison_count": len(st.session_state.comparison_results),
        "settings": st.session_state.settings,
    })
