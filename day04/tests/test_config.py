"""
Unit tests for configuration modules.
"""

import pytest
from config import Config
from ui_config import UIConfig


class TestConfig:
    """Test cases for Config class."""

    def test_config_attributes(self):
        """Test that all config attributes are defined."""
        assert hasattr(Config, "PUBMED_EMAIL")
        assert hasattr(Config, "PUBMED_API_KEY")
        assert hasattr(Config, "RATE_LIMIT_NO_KEY")
        assert hasattr(Config, "RATE_LIMIT_WITH_KEY")
        assert hasattr(Config, "YEARS_BACK")
        assert hasattr(Config, "CACHE_DIR")
        assert hasattr(Config, "DEFAULT_CACHE_AGE_DAYS")

    def test_trend_thresholds(self):
        """Test trend threshold values."""
        assert Config.TREND_HOT_THRESHOLD == 50.0
        assert Config.TREND_GROWING_THRESHOLD == 10.0
        assert Config.TREND_DECLINING_THRESHOLD == -10.0

    def test_rate_limit_delay_no_key(self):
        """Test rate limit without API key."""
        old_key = Config.PUBMED_API_KEY
        Config.PUBMED_API_KEY = None
        
        delay = Config.get_rate_limit_delay()

        Config.PUBMED_API_KEY = old_key
        assert delay == Config.RATE_LIMIT_NO_KEY
        assert delay == 0.34

    def test_rate_limit_delay_with_key(self):
        """Test rate limit with API key."""
        old_key = Config.PUBMED_API_KEY
        Config.PUBMED_API_KEY = "dummy_key"
        
        delay = Config.get_rate_limit_delay()

        Config.PUBMED_API_KEY = old_key
        assert delay == Config.RATE_LIMIT_WITH_KEY
        assert delay == 0.1

    def test_years_back(self):
        """Test years back configuration."""
        assert Config.YEARS_BACK == 20
        assert isinstance(Config.YEARS_BACK, int)

    def test_cache_settings(self):
        """Test cache configuration."""
        assert Config.CACHE_DIR == "cache"
        assert Config.DEFAULT_CACHE_AGE_DAYS == 30


class TestUIConfig:
    """Test cases for UIConfig class."""

    def test_page_config(self):
        """Test page configuration."""
        assert UIConfig.PAGE_TITLE == "Gene Trend Tracker"
        assert UIConfig.PAGE_ICON == "🧬"
        assert UIConfig.LAYOUT == "wide"

    def test_example_genes(self):
        """Test example genes list."""
        assert isinstance(UIConfig.EXAMPLE_GENES, list)
        assert len(UIConfig.EXAMPLE_GENES) > 0
        assert "TP53" in UIConfig.EXAMPLE_GENES
        assert "BRCA1" in UIConfig.EXAMPLE_GENES

    def test_status_labels(self):
        """Test status labels."""
        assert UIConfig.STATUS_HOT == "🔥 Hot Topic"
        assert UIConfig.STATUS_GROWING == "📈 Growing"
        assert UIConfig.STATUS_STABLE == "📊 Stable"
        assert UIConfig.STATUS_DECLINING == "📉 Declining"

    def test_colors(self):
        """Test color configuration."""
        assert isinstance(UIConfig.COLORS, dict)
        assert "hot" in UIConfig.COLORS
        assert "growing" in UIConfig.COLORS
        assert "stable" in UIConfig.COLORS
        assert "declining" in UIConfig.COLORS

    def test_multi_gene_colors(self):
        """Test multi-gene color palette."""
        assert isinstance(UIConfig.MULTI_GENE_COLORS, list)
        assert len(UIConfig.MULTI_GENE_COLORS) >= 8

    def test_interpretation_templates(self):
        """Test interpretation templates exist."""
        assert hasattr(UIConfig, "INTERPRETATION_HOT")
        assert hasattr(UIConfig, "INTERPRETATION_GROWING")
        assert hasattr(UIConfig, "INTERPRETATION_STABLE")
        assert hasattr(UIConfig, "INTERPRETATION_DECLINING")

    def test_message_templates(self):
        """Test message templates."""
        assert "{gene}" in UIConfig.MESSAGE_VALIDATING
        assert "{gene}" in UIConfig.MESSAGE_VALIDATED
        assert "{error}" in UIConfig.MESSAGE_ERROR

    def test_custom_css_exists(self):
        """Test custom CSS is defined."""
        assert hasattr(UIConfig, "CUSTOM_CSS")
        assert isinstance(UIConfig.CUSTOM_CSS, str)
        assert "<style>" in UIConfig.CUSTOM_CSS


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
