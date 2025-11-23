"""
Integration tests for Gene Trend Tracker.

These tests verify that different components work together correctly.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pubmed_client import PubMedClient
from data_processor import DataProcessor
from visualizer import TrendVisualizer
import tempfile
import shutil


class TestIntegration:
    """Integration tests for the application."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def processor(self, temp_cache_dir):
        """Create a data processor with temp cache."""
        return DataProcessor(cache_dir=temp_cache_dir)

    @pytest.fixture
    def visualizer(self):
        """Create a visualizer instance."""
        return TrendVisualizer()

    @patch("pubmed_client.Entrez.esearch")
    @patch("pubmed_client.Entrez.read")
    def test_full_workflow_with_cache(
        self, mock_read, mock_esearch, processor, visualizer
    ):
        """Test complete workflow from search to visualization."""
        # Mock PubMed responses
        mock_handle = MagicMock()
        mock_esearch.return_value = mock_handle

        # Validation response
        mock_read.return_value = {"Count": "100"}

        client = PubMedClient()

        # Validate gene
        assert client.validate_gene_exists("TP53") is True

        # Mock yearly search responses
        mock_read.side_effect = [{"Count": str(100 + i * 10)} for i in range(5)]

        # Get yearly counts
        yearly_counts = {}
        for year in range(2020, 2025):
            mock_read.return_value = {"Count": str(100 + (year - 2020) * 10)}
            yearly_counts[year] = client.search_gene_publications("TP53", year)

        # Cache the data
        processor.save_to_cache("TP53", yearly_counts)

        # Load from cache
        cached_data = processor.load_from_cache("TP53")
        assert cached_data is not None
        assert cached_data["gene"] == "TP53"

        # Process data
        stats = processor.process_yearly_data(yearly_counts)
        assert stats["total_publications"] > 0
        assert len(stats["years"]) == 5

        # Create visualizations
        fig = visualizer.create_timeline_chart(stats["years"], stats["counts"], "TP53")
        assert fig is not None
        assert len(fig.data) == 2

    @patch("pubmed_client.Entrez.esearch")
    @patch("pubmed_client.Entrez.read")
    def test_multi_gene_workflow(self, mock_read, mock_esearch, processor, visualizer):
        """Test workflow with multiple genes."""
        mock_handle = MagicMock()
        mock_esearch.return_value = mock_handle

        client = PubMedClient()
        genes = ["TP53", "BRCA1"]
        all_gene_data = {}

        for gene in genes:
            # Validate
            mock_read.return_value = {"Count": "100"}
            assert client.validate_gene_exists(gene) is True

            # Get yearly data (simplified)
            yearly_counts = {2020: 100, 2021: 120, 2022: 140}
            processor.save_to_cache(gene, yearly_counts)

            # Process
            stats = processor.process_yearly_data(yearly_counts)
            all_gene_data[gene] = {
                "years": stats["years"],
                "counts": stats["counts"],
            }

        # Create comparison chart
        fig = visualizer.create_multi_gene_comparison(all_gene_data)
        assert fig is not None
        assert len(fig.data) == len(genes)

    def test_trend_status_workflow(self, processor):
        """Test trend status determination workflow."""
        # Hot topic - needs significant recent growth
        yearly_counts_hot = {
            2015: 100,
            2016: 110,
            2017: 120,
            2018: 130,
            2019: 140,
            2020: 300,
            2021: 350,
            2022: 400,
            2023: 450,
            2024: 500,
        }
        stats_hot = processor.process_yearly_data(yearly_counts_hot)
        status_hot = processor.determine_trend_status(stats_hot["trend_change_percent"])
        assert "Hot Topic" in status_hot or "Growing" in status_hot

        # Declining - needs negative trend
        yearly_counts_decline = {
            2015: 500,
            2016: 480,
            2017: 460,
            2018: 440,
            2019: 420,
            2020: 300,
            2021: 280,
            2022: 260,
            2023: 240,
            2024: 220,
        }
        stats_decline = processor.process_yearly_data(yearly_counts_decline)
        status_decline = processor.determine_trend_status(
            stats_decline["trend_change_percent"]
        )
        assert "Declining" in status_decline

    def test_cache_persistence(self, processor):
        """Test that cached data persists correctly."""
        gene = "TEST_GENE"
        yearly_counts = {2020: 10, 2021: 20, 2022: 30}

        # Save
        processor.save_to_cache(gene, yearly_counts)

        # Verify file exists
        cache_path = processor._get_cache_path(gene)
        assert cache_path.exists()

        # Load in new processor instance with same cache dir
        processor2 = DataProcessor(cache_dir=str(processor.cache_dir))
        cached = processor2.load_from_cache(gene)

        assert cached is not None
        assert cached["gene"] == gene
        assert len(cached["yearly_counts"]) == 3

    def test_error_handling_invalid_gene(self):
        """Test error handling for invalid genes."""
        client = PubMedClient()

        with patch("pubmed_client.Entrez.esearch") as mock_search:
            mock_search.side_effect = Exception("API Error")

            # Should return 0 instead of raising
            count = client.search_gene_publications("INVALID_GENE")
            assert count == 0

    def test_visualization_edge_cases(self, visualizer):
        """Test visualizations with edge cases."""
        # Single year
        fig_single = visualizer.create_timeline_chart([2020], [100], "GENE1")
        assert fig_single is not None

        # Two years (minimum for growth chart)
        fig_growth = visualizer.create_yearly_growth_chart([2020, 2021], [100, 120])
        assert fig_growth is not None

        # Multi-gene with one gene
        fig_multi = visualizer.create_multi_gene_comparison(
            {"GENE1": {"years": [2020, 2021], "counts": [100, 120]}}
        )
        assert fig_multi is not None


class TestDataFlow:
    """Test data flow through the system."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_data_transformation_pipeline(self, temp_cache_dir):
        """Test complete data transformation from API to visualization."""
        # Simulate API response
        raw_yearly_data = {
            2015: 50,
            2016: 60,
            2017: 70,
            2018: 80,
            2019: 90,
            2020: 100,
            2021: 110,
            2022: 120,
            2023: 130,
            2024: 140,
        }

        # Process
        processor = DataProcessor(cache_dir=temp_cache_dir)
        stats = processor.process_yearly_data(raw_yearly_data)

        # Verify transformations
        assert stats["years"] == list(range(2015, 2025))
        assert stats["counts"] == [50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
        assert stats["total_publications"] == 950
        assert stats["average_per_year"] == 95.0
        assert stats["peak_year"] == 2024
        assert stats["peak_count"] == 140

        # Verify trend calculation
        recent_5 = sum([100, 110, 120, 130, 140])  # 600
        previous_5 = sum([50, 60, 70, 80, 90])  # 350
        expected_trend = ((recent_5 - previous_5) / previous_5) * 100
        assert abs(stats["trend_change_percent"] - expected_trend) < 0.1

    @patch("pubmed_client.Entrez.esearch")
    @patch("pubmed_client.Entrez.read")
    def test_progress_callback_integration(self, mock_read, mock_esearch):
        """Test that progress callbacks work correctly."""
        mock_handle = MagicMock()
        mock_esearch.return_value = mock_handle
        mock_read.return_value = {"Count": "100"}

        progress_calls = []

        def progress_callback(year, count, completed, total):
            progress_calls.append((year, count, completed, total))

        client = PubMedClient()
        yearly_counts = client.get_yearly_counts(
            "TEST", 2020, 2022, progress_callback=progress_callback
        )

        # Verify progress was tracked
        assert len(progress_calls) == 3
        assert progress_calls[0][0] == 2020
        assert progress_calls[1][0] == 2021
        assert progress_calls[2][0] == 2022
        assert progress_calls[2][2] == 3  # completed
        assert progress_calls[2][3] == 3  # total


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
