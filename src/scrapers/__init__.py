"""Scraper module for supermarket price scraping."""

from src.scrapers.base_scraper import BaseScraper
from src.scrapers.albert_heijn import AlbertHeijnScraper
from src.scrapers.jumbo import JumboScraper
from src.scrapers.dirk import DirkScraper
from src.scrapers.plus import PlusScraper
from src.scrapers.flink import FlinkScraper
from src.scrapers.picnic import PicnicScraper

__all__ = [
    "BaseScraper",
    "AlbertHeijnScraper",
    "JumboScraper",
    "DirkScraper",
    "PlusScraper",
    "FlinkScraper",
    "PicnicScraper",
]

SCRAPERS = {
    "albert_heijn": AlbertHeijnScraper,
    "jumbo": JumboScraper,
    "dirk": DirkScraper,
    "plus": PlusScraper,
    "flink": FlinkScraper,
    "picnic": PicnicScraper,
}
