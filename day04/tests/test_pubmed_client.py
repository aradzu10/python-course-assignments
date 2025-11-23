"""
Unit tests for PubMed Client.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pubmed_client import PubMedClient


class TestPubMedClient:
    """Test cases for PubMedClient class."""

    def test_client_initialization(self):
        """Test client initialization with and without credentials."""
        # Without credentials
        client = PubMedClient()
        assert client.email == "user@example.com"  # Default email
        assert client.api_key is None
        assert client.rate_limit_delay == 0.34

        # With credentials
        client = PubMedClient(email="test@example.com", api_key="test_key")
        assert client.email == "test@example.com"
        assert client.api_key == "test_key"
        assert client.rate_limit_delay == 0.1

    @patch("pubmed_client.Entrez.esearch")
    @patch("pubmed_client.Entrez.read")
    def test_search_gene_publications_success(self, mock_read, mock_esearch):
        """Test successful gene publication search."""
        # Mock Bio.Entrez response
        mock_handle = MagicMock()
        mock_esearch.return_value = mock_handle
        mock_read.return_value = {"Count": "1234"}

        client = PubMedClient()
        count = client.search_gene_publications("TP53")

        assert count == 1234
        assert mock_esearch.called
        assert mock_read.called
        mock_handle.close.assert_called_once()

    @patch("pubmed_client.Entrez.esearch")
    @patch("pubmed_client.Entrez.read")
    def test_search_gene_publications_with_year(self, mock_read, mock_esearch):
        """Test gene publication search with specific year."""
        mock_handle = MagicMock()
        mock_esearch.return_value = mock_handle
        mock_read.return_value = {"Count": "567"}

        client = PubMedClient()
        count = client.search_gene_publications("BRCA1", year=2020)

        assert count == 567
        # Check that esearch was called with year in query
        call_args = mock_esearch.call_args
        assert "2020[PDAT]" in call_args[1]["term"]

    @patch("pubmed_client.Entrez.esearch")
    def test_search_gene_publications_error(self, mock_esearch):
        """Test handling of API errors."""
        mock_esearch.side_effect = Exception("API Error")

        client = PubMedClient()
        count = client.search_gene_publications("INVALID")

        assert count == 0

    @patch("pubmed_client.Entrez.esearch")
    @patch("pubmed_client.Entrez.read")
    def test_validate_gene_exists(self, mock_read, mock_esearch):
        """Test gene validation."""
        # Mock response with results
        mock_handle = MagicMock()
        mock_esearch.return_value = mock_handle
        mock_read.return_value = {"Count": "100"}

        client = PubMedClient()
        assert client.validate_gene_exists("TP53") is True

        # Mock response with no results
        mock_read.return_value = {"Count": "0"}
        assert client.validate_gene_exists("NOTGENE") is False

    @patch.object(PubMedClient, "search_gene_publications")
    def test_get_yearly_counts(self, mock_search):
        """Test fetching yearly counts."""
        # Mock search results
        mock_search.side_effect = [10, 20, 30]

        client = PubMedClient()
        yearly_counts = client.get_yearly_counts("TEST", 2020, 2022)

        assert len(yearly_counts) == 3
        assert yearly_counts[2020] == 10
        assert yearly_counts[2021] == 20
        assert yearly_counts[2022] == 30
        assert mock_search.call_count == 3

    @patch.object(PubMedClient, "search_gene_publications")
    def test_get_yearly_counts_with_progress_callback(self, mock_search):
        """Test fetching yearly counts with progress callback."""
        # Mock search results
        mock_search.side_effect = [10, 20, 30]

        # Track progress callback calls
        progress_calls = []

        def progress_callback(year, count, completed, total):
            progress_calls.append((year, count, completed, total))

        client = PubMedClient()
        yearly_counts = client.get_yearly_counts(
            "TEST", 2020, 2022, progress_callback=progress_callback
        )

        assert len(yearly_counts) == 3
        assert len(progress_calls) == 3
        assert progress_calls[0] == (2020, 10, 1, 3)
        assert progress_calls[1] == (2021, 20, 2, 3)
        assert progress_calls[2] == (2022, 30, 3, 3)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
