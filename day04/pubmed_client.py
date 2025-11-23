"""
PubMed API Client for fetching publication counts.

This module provides functionality to query the NCBI PubMed database
and retrieve publication counts for specific genes over time.
"""

from Bio import Entrez
import time
from typing import Dict, Optional, Callable
from datetime import datetime
from config import Config


class PubMedClient:
    """Client for interacting with the NCBI E-utilities API via Bio.Entrez."""

    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the PubMed client.

        Args:
            email: Optional email for NCBI API (recommended for better rate limits)
            api_key: Optional API key for higher rate limits
        """
        self.email = email or Config.PUBMED_EMAIL
        self.api_key = api_key or Config.PUBMED_API_KEY
        self.rate_limit_delay = Config.get_rate_limit_delay(bool(self.api_key))

        # Configure Entrez
        Entrez.email = self.email
        if self.api_key:
            Entrez.api_key = self.api_key

    def search_gene_publications(self, gene: str, year: Optional[int] = None) -> int:
        """
        Search PubMed for publications mentioning a specific gene.

        Args:
            gene: Gene name or symbol to search for
            year: Optional specific year to filter results

        Returns:
            Number of publications found
        """
        # Build the search query
        query = f"{gene}[Gene Name] OR {gene}[Title/Abstract]"
        if year:
            query += f" AND {year}[PDAT]"

        try:
            # Add delay to respect rate limits
            time.sleep(self.rate_limit_delay)

            # Use Bio.Entrez to search
            handle = Entrez.esearch(db="pubmed", term=query, retmax=0)
            record = Entrez.read(handle)
            handle.close()

            # Record is a dictionary-like object
            count_str = str(record.get("Count", "0"))  # type: ignore
            count = int(count_str)
            return count

        except Exception as e:
            print(f"Error fetching data from PubMed: {e}")
            return 0

    def get_yearly_counts(
        self,
        gene: str,
        start_year: int,
        end_year: int,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[int, int]:
        """
        Get publication counts for a gene across multiple years.

        Args:
            gene: Gene name or symbol to search for
            start_year: Starting year for the search
            end_year: Ending year for the search
            progress_callback: Optional callback function to report progress (year, count, total_years)

        Returns:
            Dictionary mapping years to publication counts
        """
        yearly_counts = {}
        total_years = end_year - start_year + 1

        print(f"Fetching publication data for {gene} ({start_year}-{end_year})...")

        for idx, year in enumerate(range(start_year, end_year + 1)):
            count = self.search_gene_publications(gene, year)
            yearly_counts[year] = count
            print(f"  {year}: {count} publications")

            # Call progress callback if provided
            if progress_callback:
                progress_callback(year, count, idx + 1, total_years)

        return yearly_counts

    def validate_gene_exists(self, gene: str) -> bool:
        """
        Check if a gene exists in PubMed database.

        Args:
            gene: Gene name or symbol to validate

        Returns:
            True if at least one publication is found
        """
        count = self.search_gene_publications(gene)
        return count > 0


def main():
    """Example usage of the PubMed client."""
    client = PubMedClient()

    # Example: Search for TP53 gene
    gene = "TP53"
    current_year = datetime.now().year
    start_year = current_year - 20

    print(f"\n=== Gene Trend Tracker ===")
    print(f"Analyzing: {gene}\n")

    # Check if gene exists
    if not client.validate_gene_exists(gene):
        print(f"Warning: No publications found for '{gene}'")
        return

    # Get yearly counts
    yearly_data = client.get_yearly_counts(gene, start_year, current_year)

    # Display summary
    total = sum(yearly_data.values())
    print(f"\nTotal publications: {total}")
    print(f"Average per year: {total // len(yearly_data)}")


if __name__ == "__main__":
    main()
