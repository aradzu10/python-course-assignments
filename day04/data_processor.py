"""
Data Processor for Gene Trend Tracker.

Handles data processing, caching, and organization of publication data.
"""

import json
import os
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path
from config import Config


class DataProcessor:
    """Process and cache gene publication data."""

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the data processor.

        Args:
            cache_dir: Directory for caching data (defaults to Config.CACHE_DIR)
        """
        self.cache_dir = Path(cache_dir or Config.CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_path(self, gene: str) -> Path:
        """
        Get the cache file path for a specific gene.

        Args:
            gene: Gene name or symbol

        Returns:
            Path to cache file
        """
        # Sanitize gene name for filename
        safe_gene = "".join(c for c in gene if c.isalnum() or c in "-_").lower()
        return self.cache_dir / f"{safe_gene}.json"

    def load_from_cache(self, gene: str, max_age_days: int = 30) -> Optional[Dict]:
        """
        Load gene data from cache if available and not too old.

        Args:
            gene: Gene name or symbol
            max_age_days: Maximum age of cache in days

        Returns:
            Cached data dictionary or None if not available/expired
        """
        cache_path = self._get_cache_path(gene)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r") as f:
                data = json.load(f)

            # Check cache age
            cache_date = datetime.fromisoformat(data.get("cached_at", "2000-01-01"))
            age_days = (datetime.now() - cache_date).days

            if age_days > max_age_days:
                print(f"Cache expired (age: {age_days} days)")
                return None

            print(f"Loaded from cache (age: {age_days} days)")
            return data

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error reading cache: {e}")
            return None

    def save_to_cache(
        self, gene: str, yearly_counts: Dict[int, int], metadata: Optional[Dict] = None
    ):
        """
        Save gene data to cache.

        Args:
            gene: Gene name or symbol
            yearly_counts: Dictionary of year -> publication count
            metadata: Optional additional metadata
        """
        cache_path = self._get_cache_path(gene)

        data = {
            "gene": gene,
            "cached_at": datetime.now().isoformat(),
            "yearly_counts": {
                str(year): count for year, count in yearly_counts.items()
            },
            "metadata": metadata or {},
        }

        try:
            with open(cache_path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Data cached for {gene}")
        except IOError as e:
            print(f"Error writing cache: {e}")

    def process_yearly_data(self, yearly_counts: Dict[int, int]) -> Dict:
        """
        Process yearly publication counts and generate statistics.

        Args:
            yearly_counts: Dictionary of year -> publication count

        Returns:
            Processed data with statistics
        """
        if not yearly_counts:
            return {}

        years = sorted(yearly_counts.keys())
        counts = [yearly_counts[year] for year in years]

        total_pubs = sum(counts)
        avg_pubs = total_pubs / len(counts) if counts else 0
        peak_year = max(yearly_counts.items(), key=lambda x: x[1])

        # Calculate recent trend (last 5 years vs previous 5 years)
        if len(years) >= 10:
            recent_5 = sum(counts[-5:])
            previous_5 = sum(counts[-10:-5])
            trend_change = (
                ((recent_5 - previous_5) / previous_5 * 100) if previous_5 > 0 else 0
            )
        else:
            recent_5 = sum(counts[-5:]) if len(counts) >= 5 else sum(counts)
            trend_change = 0

        return {
            "years": years,
            "counts": counts,
            "total_publications": total_pubs,
            "average_per_year": round(avg_pubs, 1),
            "peak_year": peak_year[0],
            "peak_count": peak_year[1],
            "recent_5_year_count": recent_5,
            "trend_change_percent": round(trend_change, 1),
        }

    def determine_trend_status(self, trend_change_percent: float) -> str:
        """
        Determine the trend status based on percentage change.

        Args:
            trend_change_percent: Percentage change in recent activity

        Returns:
            Status string
        """
        if trend_change_percent > Config.TREND_HOT_THRESHOLD:
            return "🔥 Hot Topic"
        elif trend_change_percent > Config.TREND_GROWING_THRESHOLD:
            return "📈 Growing"
        elif trend_change_percent > Config.TREND_DECLINING_THRESHOLD:
            return "📊 Stable"
        else:
            return "📉 Declining"

    def clear_cache(self):
        """Clear all cached data."""
        import shutil

        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(exist_ok=True)
            print("Cache cleared")

    def list_cached_genes(self) -> list:
        """
        List all genes that have cached data.

        Returns:
            List of gene names
        """
        if not self.cache_dir.exists():
            return []

        cached_genes = []
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                    cached_genes.append(data.get("gene", cache_file.stem))
            except (json.JSONDecodeError, IOError):
                continue

        return sorted(cached_genes)


def main():
    """Example usage of the data processor."""
    processor = DataProcessor()

    # Example data
    test_data = {
        2004: 1500,
        2005: 1600,
        2006: 1700,
        2007: 1800,
        2008: 1900,
        2009: 2000,
        2010: 2100,
        2011: 2200,
        2012: 2400,
        2013: 2600,
        2014: 2800,
        2015: 3000,
        2016: 3200,
        2017: 3400,
        2018: 3600,
        2019: 3900,
        2020: 4200,
        2021: 4500,
        2022: 4800,
        2023: 5100,
        2024: 5400,
    }

    # Process and save
    gene = "TP53"
    processor.save_to_cache(gene, test_data)

    # Load and process
    cached = processor.load_from_cache(gene)
    if cached:
        yearly_counts = {
            int(year): count for year, count in cached["yearly_counts"].items()
        }
        stats = processor.process_yearly_data(yearly_counts)

        print(f"\n=== Statistics for {gene} ===")
        print(f"Total publications: {stats['total_publications']}")
        print(f"Average per year: {stats['average_per_year']}")
        print(f"Peak year: {stats['peak_year']} ({stats['peak_count']} publications)")
        print(f"Recent 5-year count: {stats['recent_5_year_count']}")
        print(f"Trend: {stats['trend_change_percent']}%")
        print(
            f"Status: {processor.determine_trend_status(stats['trend_change_percent'])}"
        )

    # List cached genes
    print(f"\nCached genes: {processor.list_cached_genes()}")


if __name__ == "__main__":
    main()
