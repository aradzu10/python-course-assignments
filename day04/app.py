"""
Gene Trend Tracker - Main Application

This is the main entry point that orchestrates the application for
tracking research trends of genes or topics. It connects the UI layer
with the business logic layer.
"""

import streamlit as st
from datetime import datetime
import time
from typing import Dict

from config import Config
from pubmed_client import PubMedClient
from data_processor import DataProcessor
from ui_components import UIComponents


class GeneTracker:
    """Main application controller."""

    def __init__(self):
        """Initialize the application."""
        self.ui = UIComponents()
        self.client = None
        self.processor = None
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if "gene_data" not in st.session_state:
            st.session_state.gene_data = None
        if "current_gene" not in st.session_state:
            st.session_state.current_gene = None
        if "gene_history" not in st.session_state:
            st.session_state.gene_history = {}
        if "selected_genes" not in st.session_state:
            st.session_state.selected_genes = []

    def get_client(self) -> PubMedClient:
        """Get or create PubMed client instance."""
        if self.client is None:
            self.client = PubMedClient()
        return self.client

    def get_processor(self) -> DataProcessor:
        """Get or create DataProcessor instance."""
        if self.processor is None:
            self.processor = DataProcessor()
        return self.processor

    def handle_example_click(self, gene: str):
        """Handle example item button click."""
        st.session_state.current_gene = gene
        st.rerun()

    def handle_clear_cache(self):
        """Handle clear cache button click."""
        processor = self.get_processor()
        processor.clear_cache()
        st.session_state.gene_data = None

    def handle_clear_history(self):
        """Handle clear history button click."""
        st.session_state.gene_history = {}
        st.session_state.selected_genes = []
        st.rerun()

    def process_gene_search(self, gene: str, use_cache: bool, cache_days: int):
        """
        Process a gene or topic search request.

        Args:
            gene: Gene or topic name
            use_cache: Whether to use cached data
            cache_days: Maximum cache age in days
        """
        # Mandatory validation
        gene = gene.strip()
        if not gene:
            self.ui.show_error(self.ui.config.MESSAGE_ENTER_GENE)
            return

        try:
            client = self.get_client()
            processor = self.get_processor()

            # Try to load from cache first
            cached_data = None
            if use_cache:
                cached_data = processor.load_from_cache(gene, cache_days)

            if cached_data:
                yearly_counts = {
                    int(year): count
                    for year, count in cached_data["yearly_counts"].items()
                }
                self.ui.show_info(self.ui.config.MESSAGE_CACHED)
            else:
                # Validate gene
                with self.ui.show_spinner(
                    self.ui.config.MESSAGE_VALIDATING.format(gene=gene)
                ):
                    if not client.validate_gene_exists(gene):
                        self.ui.show_error(
                            self.ui.config.MESSAGE_VALIDATION_FAILED.format(gene=gene)
                        )
                        return
                    self.ui.show_success(
                        self.ui.config.MESSAGE_VALIDATED.format(gene=gene)
                    )

                # Fetch data with progress
                yearly_counts = self._fetch_with_progress(gene, client)

                # Cache the data
                processor.save_to_cache(gene, yearly_counts)

            # Process data
            stats = processor.process_yearly_data(yearly_counts)
            trend_status = processor.determine_trend_status(
                stats["trend_change_percent"]
            )

            # Store results
            gene_data = {
                "gene": gene,
                "yearly_counts": yearly_counts,
                "stats": stats,
                "trend_status": trend_status,
            }

            st.session_state.gene_data = gene_data
            st.session_state.gene_history[gene] = gene_data

            # Auto-select for comparison
            if gene not in st.session_state.selected_genes:
                st.session_state.selected_genes.append(gene)

        except Exception as e:
            self.ui.show_error(self.ui.config.MESSAGE_ERROR.format(error=str(e)))
            st.session_state.gene_data = None

    def _fetch_with_progress(self, gene: str, client: PubMedClient) -> Dict[int, int]:
        """
        Fetch gene data with progress indicators.

        Args:
            gene: Gene name
            client: PubMed client instance

        Returns:
            Dictionary mapping years to publication counts
        """
        current_year = datetime.now().year
        start_year = current_year - Config.YEARS_BACK
        total_years = current_year - start_year + 1

        # Create progress UI
        progress_bar, status_text = self.ui.create_progress_bar(
            self.ui.config.MESSAGE_FETCHING.format(gene=gene)
        )

        def progress_callback(year, count, completed, total):
            """Progress callback for data fetch."""
            progress = completed / total
            self.ui.update_progress(
                progress_bar,
                status_text,
                progress,
                self.ui.config.MESSAGE_FETCHING_PROGRESS.format(
                    gene=gene, year=year, completed=completed, total=total
                ),
                self.ui.config.MESSAGE_YEAR_COUNT.format(year=year, count=count),
            )

        # Fetch data
        yearly_counts = client.get_yearly_counts(
            gene, start_year, current_year, progress_callback=progress_callback
        )

        # Complete progress
        self.ui.update_progress(
            progress_bar,
            status_text,
            1.0,
            self.ui.config.MESSAGE_FETCH_COMPLETE,
            "",
        )
        status_text.empty()
        time.sleep(0.5)
        progress_bar.empty()

        return yearly_counts

    def run(self):
        """Run the main application."""
        # Setup page
        self.ui.setup_page_config()
        self.ui.apply_custom_css()

        # Render header
        self.ui.render_header()

        # Render sidebar and get settings
        use_cache, cache_days = self.ui.render_sidebar(
            on_example_click=self.handle_example_click,
            on_clear_cache=self.handle_clear_cache,
        )

        # Render input section
        gene_input, track_button = self.ui.render_input_section(
            st.session_state.current_gene
        )

        # Render comparison section
        selected_genes = self.ui.render_comparison_section(
            st.session_state.gene_history,
            st.session_state.selected_genes,
            on_clear_history=self.handle_clear_history,
        )
        st.session_state.selected_genes = selected_genes

        # Process search
        if track_button and gene_input:
            st.session_state.current_gene = gene_input
            self.process_gene_search(gene_input, use_cache, cache_days)

        # Display results
        if st.session_state.gene_data:
            self.ui.render_results(
                st.session_state.gene_data,
                st.session_state.selected_genes,
                st.session_state.gene_history,
            )
        else:
            self.ui.render_welcome_message()


def main():
    """Application entry point."""
    app = GeneTracker()
    app.run()


if __name__ == "__main__":
    main()
