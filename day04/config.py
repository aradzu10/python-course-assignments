"""
Configuration settings for Gene Trend Tracker application.
"""

import os
from typing import Optional


class Config:
    """Application configuration settings."""

    # PubMed API Settings
    PUBMED_EMAIL: Optional[str] = os.getenv("PUBMED_EMAIL", "user@example.com")
    PUBMED_API_KEY: Optional[str] = os.getenv("PUBMED_API_KEY", None)

    # Rate limiting (seconds between requests)
    RATE_LIMIT_NO_KEY: float = 0.34
    RATE_LIMIT_WITH_KEY: float = 0.1

    # Data settings
    YEARS_BACK: int = 20
    CACHE_DIR: str = ".cache"
    DEFAULT_CACHE_AGE_DAYS: int = 30

    # Trend thresholds (percentage change)
    TREND_HOT_THRESHOLD: float = 50.0
    TREND_GROWING_THRESHOLD: float = 10.0
    TREND_DECLINING_THRESHOLD: float = -10.0

    # Analysis settings
    RECENT_YEARS_WINDOW: int = 5
    PREVIOUS_YEARS_WINDOW: int = 5

    @classmethod
    def get_rate_limit_delay(cls, has_api_key: bool | None = None) -> float:
        """
        Get the appropriate rate limit delay.

        Args:
            has_api_key: Whether an API key is configured (defaults to checking Config.PUBMED_API_KEY)

        Returns:
            Delay in seconds between API requests
        """
        if has_api_key is None:
            has_api_key = bool(Config.PUBMED_API_KEY)
        return cls.RATE_LIMIT_WITH_KEY if has_api_key else cls.RATE_LIMIT_NO_KEY
