"""
Unit tests for Data Processor.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from data_processor import DataProcessor


class TestDataProcessor:
    """Test cases for DataProcessor class."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def processor(self, temp_cache_dir):
        """Create a DataProcessor instance with temporary cache."""
        return DataProcessor(cache_dir=temp_cache_dir)

    def test_processor_initialization(self, temp_cache_dir):
        """Test processor initialization."""
        processor = DataProcessor(cache_dir=temp_cache_dir)
        assert processor.cache_dir.exists()
        assert processor.cache_dir == Path(temp_cache_dir)

    def test_save_and_load_cache(self, processor):
        """Test saving and loading cache data."""
        gene = "TP53"
        yearly_counts = {2020: 100, 2021: 150, 2022: 200}

        # Save to cache
        processor.save_to_cache(gene, yearly_counts)

        # Load from cache
        cached_data = processor.load_from_cache(gene)

        assert cached_data is not None
        assert cached_data["gene"] == gene
        assert len(cached_data["yearly_counts"]) == 3

    def test_cache_expiration(self, processor, temp_cache_dir):
        """Test that old cache is not loaded."""
        gene = "BRCA1"
        yearly_counts = {2020: 50, 2021: 60}

        # Save to cache
        processor.save_to_cache(gene, yearly_counts)

        # Manually modify cache timestamp to be old
        cache_path = processor._get_cache_path(gene)
        with open(cache_path, "r") as f:
            data = json.load(f)

        old_date = datetime.now() - timedelta(days=40)
        data["cached_at"] = old_date.isoformat()

        with open(cache_path, "w") as f:
            json.dump(data, f)

        # Try to load with max_age_days=30
        cached_data = processor.load_from_cache(gene, max_age_days=30)
        assert cached_data is None

    def test_process_yearly_data(self, processor):
        """Test processing of yearly data."""
        yearly_counts = {
            2015: 100,
            2016: 120,
            2017: 140,
            2018: 160,
            2019: 180,
            2020: 200,
            2021: 220,
            2022: 240,
            2023: 260,
            2024: 280,
        }

        stats = processor.process_yearly_data(yearly_counts)

        assert stats["total_publications"] == 1900
        assert 189.99 <= stats["average_per_year"] <= 190.01
        assert stats["peak_year"] == 2024
        assert stats["peak_count"] == 280
        assert len(stats["years"]) == 10
        assert len(stats["counts"]) == 10

    def test_determine_trend_status(self, processor):
        """Test trend status determination."""
        assert processor.determine_trend_status(60) == "🔥 Hot Topic"
        assert processor.determine_trend_status(30) == "📈 Growing"
        assert processor.determine_trend_status(5) == "📊 Stable"
        assert processor.determine_trend_status(-20) == "📉 Declining"

    def test_clear_cache(self, processor):
        """Test clearing cache."""
        # Add some cache files
        processor.save_to_cache("GENE1", {2020: 10})
        processor.save_to_cache("GENE2", {2020: 20})

        # Clear cache
        processor.clear_cache()

        # Verify cache is empty but directory exists
        assert processor.cache_dir.exists()
        assert len(list(processor.cache_dir.glob("*.json"))) == 0

    def test_list_cached_genes(self, processor):
        """Test listing cached genes."""
        # Initially empty
        assert processor.list_cached_genes() == []

        # Add some genes
        processor.save_to_cache("TP53", {2020: 100})
        processor.save_to_cache("BRCA1", {2020: 50})
        processor.save_to_cache("EGFR", {2020: 75})

        cached_genes = processor.list_cached_genes()
        assert len(cached_genes) == 3
        assert "BRCA1" in cached_genes
        assert "EGFR" in cached_genes
        assert "TP53" in cached_genes

    def test_sanitized_gene_names(self, processor):
        """Test that gene names are properly sanitized for filenames."""
        gene = "ABC-123_test"
        yearly_counts = {2020: 10}

        processor.save_to_cache(gene, yearly_counts)
        cache_path = processor._get_cache_path(gene)

        # Verify the file was created with sanitized name
        assert cache_path.exists()
        assert cache_path.name == "abc-123_test.json"

    def test_process_empty_data(self, processor):
        """Test processing empty data."""
        stats = processor.process_yearly_data({})
        assert stats == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
