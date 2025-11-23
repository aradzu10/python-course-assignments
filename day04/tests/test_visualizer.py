"""
Unit tests for Visualizer.
"""

import pytest
from visualizer import TrendVisualizer
import plotly.graph_objects as go


class TestTrendVisualizer:
    """Test cases for TrendVisualizer class."""

    @pytest.fixture
    def visualizer(self):
        """Create a TrendVisualizer instance."""
        return TrendVisualizer()

    @pytest.fixture
    def sample_data(self):
        """Provide sample data for testing."""
        years = list(range(2010, 2025))
        counts = [100 * (1 + i * 0.1) for i in range(len(years))]
        return years, [int(c) for c in counts]

    def test_visualizer_initialization(self, visualizer):
        """Test visualizer initialization."""
        assert visualizer is not None
        assert hasattr(visualizer, "color_scheme")
        assert len(visualizer.color_scheme) == 4

    def test_create_timeline_chart(self, visualizer, sample_data):
        """Test creating timeline chart."""
        years, counts = sample_data
        fig = visualizer.create_timeline_chart(years, counts, "TP53")

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2  # Bar chart + trend line
        assert fig.data[0].type == "bar"
        assert fig.data[1].type == "scatter"

    def test_create_recent_comparison_chart(self, visualizer):
        """Test creating comparison chart."""
        fig = visualizer.create_recent_comparison_chart(1000, 800)

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == "bar"

    def test_create_growth_indicator(self, visualizer):
        """Test creating growth indicator."""
        fig = visualizer.create_growth_indicator(45.5)

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == "indicator"

    def test_create_yearly_growth_chart(self, visualizer, sample_data):
        """Test creating yearly growth chart."""
        years, counts = sample_data
        fig = visualizer.create_yearly_growth_chart(years, counts)

        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1
        if len(fig.data) > 0:
            assert fig.data[0].type == "bar"

    def test_create_yearly_growth_chart_insufficient_data(self, visualizer):
        """Test growth chart with insufficient data."""
        fig = visualizer.create_yearly_growth_chart([2020], [100])

        assert isinstance(fig, go.Figure)
        # Should return empty figure with only 1 data point
        assert len(fig.data) == 0

    def test_timeline_chart_single_year(self, visualizer):
        """Test timeline chart with single year."""
        fig = visualizer.create_timeline_chart([2020], [100], "TEST")

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2  # Still creates both traces

    def test_comparison_chart_values(self, visualizer):
        """Test comparison chart with specific values."""
        recent = 5000
        previous = 3000

        fig = visualizer.create_recent_comparison_chart(recent, previous)

        assert isinstance(fig, go.Figure)
        # Verify the values are in the chart
        assert fig.data[0].y[0] == previous
        assert fig.data[0].y[1] == recent


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
