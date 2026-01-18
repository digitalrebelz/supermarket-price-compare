"""Application settings using pydantic-settings."""

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "sqlite:///data/supermarket.db"

    # Scraping
    scrape_rate_limit: float = 2.0
    scrape_max_retries: int = 3
    scrape_timeout: int = 30000

    # Logging
    log_level: str = "INFO"

    # UI
    streamlit_port: int = 8501

    # Paths
    base_dir: Path = Path(__file__).parent.parent.parent
    data_dir: Path = base_dir / "data"
    logs_dir: Path = base_dir / "logs"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
