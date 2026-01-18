#!/usr/bin/env python3
"""Seed database with initial supermarket data."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import get_db
from src.database.crud import upsert_supermarket
from src.config.constants import SUPERMARKETS
from loguru import logger


def seed_supermarkets():
    """Seed supermarket data into database."""
    db_manager = get_db()

    with db_manager.get_session() as session:
        for name, config in SUPERMARKETS.items():
            supermarket = upsert_supermarket(
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
            logger.info(f"Seeded supermarket: {supermarket.display_name}")

    logger.info("Database seeding complete!")


if __name__ == "__main__":
    seed_supermarkets()
