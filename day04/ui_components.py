"""
UI components for the Gene Trend Tracker application.

This module handles all Streamlit UI rendering for gene and topic analysis,
keeping the UI layer separate from business logic.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Callable
from ui_config import UIConfig
from visualizer import TrendVisualizer


class UIComponents:
    """Handles all UI rendering for the application."""

    def __init__(self):
        """Initialize UI components."""
        self.config = UIConfig()
        self.visualizer = TrendVisualizer()

    def setup_page_config(self):
        """Configure the Streamlit page."""
        st.set_page_config(
            page_title=self.config.PAGE_TITLE,
            page_icon=self.config.PAGE_ICON,
            layout=self.config.LAYOUT,
            initial_sidebar_state=self.config.INITIAL_SIDEBAR_STATE,
        )

    def apply_custom_css(self):
        """Apply custom CSS styles."""
        st.markdown(self.config.CUSTOM_CSS, unsafe_allow_html=True)

    def render_header(self):
        """Render the main header."""
        st.markdown(
            f'<div class="main-header">{self.config.MAIN_HEADER}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="sub-header">{self.config.SUB_HEADER}</div>',
            unsafe_allow_html=True,
        )

    def render_sidebar(
        self,
        on_example_click: Callable[[str], None],
        on_clear_cache: Callable[[], None],
    ) -> tuple[bool, int]:
        """
        Render the sidebar.

        Args:
            on_example_click: Callback when example item is clicked
            on_clear_cache: Callback when clear cache is clicked

        Returns:
            Tuple of (use_cache, cache_days)
        """
        with st.sidebar:
            # About section
            st.header(self.config.SIDEBAR_ABOUT_TITLE)
            st.write(self.config.SIDEBAR_ABOUT_TEXT)

            # How to use section
            st.header(self.config.SIDEBAR_HOW_TO_TITLE)
            st.write(self.config.SIDEBAR_HOW_TO_TEXT)

            # Example items
            st.header(self.config.SIDEBAR_EXAMPLES_TITLE)
            for gene in self.config.EXAMPLE_GENES:
                if st.button(gene, key=f"example_{gene}", width="stretch"):
                    on_example_click(gene)

            st.divider()

            # Settings
            st.header(self.config.SIDEBAR_SETTINGS_TITLE)
            use_cache = st.checkbox(
                self.config.SETTING_USE_CACHE_LABEL,
                value=True,
                help=self.config.SETTING_USE_CACHE_HELP,
            )
            cache_days = st.slider(
                self.config.SETTING_CACHE_AGE_LABEL,
                1,
                90,
                30,
                help=self.config.SETTING_CACHE_AGE_HELP,
            )

            if st.button(self.config.BUTTON_CLEAR_CACHE, width="stretch"):
                on_clear_cache()
                st.success(self.config.MESSAGE_CACHE_CLEARED)

        return use_cache, cache_days

    def render_input_section(self, current_gene: Optional[str]) -> tuple[str, bool]:
        """
        Render the input section for genes or topics.

        Args:
            current_gene: Current gene or topic in session state

        Returns:
            Tuple of (gene_input, track_button_clicked)
        """
        col1, col2 = st.columns([3, 1])

        with col1:
            gene_input = st.text_input(
                self.config.INPUT_GENE_LABEL,
                value=current_gene or "",
                placeholder=self.config.INPUT_GENE_PLACEHOLDER,
                help=self.config.INPUT_GENE_HELP,
            )

        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            track_button = st.button(
                self.config.BUTTON_TRACK_GENE,
                type="primary",
                width="stretch",
                disabled=not gene_input or gene_input.strip() == "",
            )

        return gene_input, track_button

    def render_comparison_section(
        self,
        gene_history: Dict[str, dict],
        selected_genes: List[str],
        on_clear_history: Callable[[], None],
    ) -> List[str]:
        """
        Render the multi-item comparison section.

        Args:
            gene_history: Dictionary of all searched items (genes or topics)
            selected_genes: Currently selected items
            on_clear_history: Callback when clear history is clicked

        Returns:
            Updated list of selected items
        """
        if not gene_history:
            return []

        st.subheader(self.config.SECTION_COMPARISON_TITLE)
        col1, col2 = st.columns([3, 1])

        with col1:
            available_genes = list(gene_history.keys())
            selected = st.multiselect(
                self.config.MULTISELECT_LABEL,
                options=available_genes,
                default=selected_genes if selected_genes else available_genes[-1:],
                help=self.config.MULTISELECT_HELP,
            )

        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button(self.config.BUTTON_CLEAR_HISTORY, width="stretch"):
                on_clear_history()

        return selected

    def show_spinner(self, message: str):
        """Show a spinner with a message."""
        return st.spinner(message)

    def show_info(self, message: str):
        """Show an info message."""
        st.info(message)

    def show_success(self, message: str):
        """Show a success message."""
        st.success(message)

    def show_error(self, message: str):
        """Show an error message."""
        st.error(message)

    def create_progress_bar(self, initial_text: str):
        """
        Create a progress bar.

        Args:
            initial_text: Initial text to display

        Returns:
            Tuple of (progress_bar, status_text)
        """
        progress_bar = st.progress(0, text=initial_text)
        status_text = st.empty()
        return progress_bar, status_text

    def update_progress(
        self, progress_bar, status_text, progress: float, message: str, status: str
    ):
        """
        Update progress bar and status text.

        Args:
            progress_bar: Progress bar object
            status_text: Status text object
            progress: Progress value (0.0 to 1.0)
            message: Progress message
            status: Status text
        """
        progress_bar.progress(progress, text=message)
        status_text.text(status)

    def render_metrics(self, stats: Dict):
        """
        Render key metrics.

        Args:
            stats: Statistics dictionary
        """
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label=self.config.METRIC_TOTAL_LABEL,
                value=f"{stats['total_publications']:,}",
            )

        with col2:
            st.metric(
                label=self.config.METRIC_AVERAGE_LABEL,
                value=f"{stats['average_per_year']:.0f}",
            )

        with col3:
            st.metric(
                label=self.config.METRIC_PEAK_LABEL,
                value=stats["peak_year"],
                delta=f"{stats['peak_count']:,} pubs",
            )

        with col4:
            st.metric(
                label=self.config.METRIC_RECENT_LABEL,
                value=f"{stats['recent_5_year_count']:,}",
                delta=f"{stats['trend_change_percent']:+.1f}%",
            )

    def render_trend_status(self, trend_status: str):
        """
        Render trend status badge.

        Args:
            trend_status: Trend status string
        """
        st.markdown(self.config.SECTION_TREND_STATUS)
        status_class = (
            trend_status.split()[1].lower()
            if len(trend_status.split()) > 1
            else "stable"
        )
        st.markdown(
            f'<div class="status-{status_class}">{trend_status}</div>',
            unsafe_allow_html=True,
        )

    def render_timeline_chart(self, years: List[int], counts: List[int], gene: str):
        """Render the main timeline chart."""
        st.subheader(self.config.SECTION_TIMELINE)
        fig = self.visualizer.create_timeline_chart(years, counts, gene)
        st.plotly_chart(fig, width="stretch")

    def render_multi_gene_comparison(
        self, selected_genes: List[str], gene_history: Dict[str, dict]
    ):
        """
        Render multi-item comparison chart and table.

        Args:
            selected_genes: List of selected items (genes or topics)
            gene_history: Dictionary of item data
        """
        if len(selected_genes) <= 1:
            return

        st.divider()
        st.subheader(self.config.SECTION_MULTI_GENE)

        # Prepare comparison data
        comparison_data = {}
        for gene in selected_genes:
            if gene in gene_history:
                gene_info = gene_history[gene]
                comparison_data[gene] = {
                    "years": gene_info["stats"]["years"],
                    "counts": gene_info["stats"]["counts"],
                }

        if len(comparison_data) > 1:
            # Render comparison chart
            fig = self.visualizer.create_multi_gene_comparison(comparison_data)
            st.plotly_chart(fig, width="stretch")

            # Render comparison table
            st.subheader(self.config.SECTION_COMPARISON_SUMMARY)
            table_data = []
            for gene in selected_genes:
                if gene in gene_history:
                    stats = gene_history[gene]["stats"]
                    table_data.append(
                        {
                            self.config.TABLE_COL_GENE: gene,
                            self.config.TABLE_COL_TOTAL: f"{stats['total_publications']:,}",
                            self.config.TABLE_COL_AVERAGE: f"{stats['average_per_year']:.0f}",
                            self.config.TABLE_COL_PEAK: stats["peak_year"],
                            self.config.TABLE_COL_TREND: f"{stats['trend_change_percent']:+.1f}%",
                            self.config.TABLE_COL_STATUS: gene_history[gene][
                                "trend_status"
                            ],
                        }
                    )

            df = pd.DataFrame(table_data)
            st.dataframe(df, width="stretch", hide_index=True)

    def render_additional_charts(self, stats: Dict):
        """
        Render additional analysis charts.

        Args:
            stats: Statistics dictionary
        """
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(self.config.SECTION_GROWTH_INDICATOR)
            fig = self.visualizer.create_growth_indicator(stats["trend_change_percent"])
            st.plotly_chart(fig, width="stretch")

        with col2:
            st.subheader(self.config.SECTION_YOY_GROWTH)
            fig = self.visualizer.create_yearly_growth_chart(
                stats["years"], stats["counts"]
            )
            st.plotly_chart(fig, width="stretch")

        # 5-year comparison chart
        if len(stats["counts"]) >= 10:
            st.subheader(self.config.SECTION_ACTIVITY_COMPARISON)
            recent_5 = stats["recent_5_year_count"]
            previous_5 = sum(stats["counts"][-10:-5])
            fig = self.visualizer.create_recent_comparison_chart(recent_5, previous_5)
            st.plotly_chart(fig, width="stretch")

    def render_interpretation(self, stats: Dict, trend_status: str):
        """
        Render interpretation section.

        Args:
            stats: Statistics dictionary
            trend_status: Trend status string
        """
        st.divider()
        st.subheader(self.config.SECTION_INTERPRETATION)

        interpretation = self.get_interpretation(stats, trend_status)
        st.info(interpretation)

    def get_interpretation(self, stats: Dict, trend_status: str) -> str:
        """
        Generate interpretation text based on trend status.

        Args:
            stats: Statistics dictionary
            trend_status: Trend status string

        Returns:
            Interpretation text
        """
        params = {
            "total": stats["total_publications"],
            "trend": stats["trend_change_percent"],
            "peak_year": stats["peak_year"],
            "peak_count": stats["peak_count"],
        }

        if "Hot Topic" in trend_status:
            return self.config.INTERPRETATION_HOT.format(**params)
        elif "Growing" in trend_status:
            return self.config.INTERPRETATION_GROWING.format(**params)
        elif "Stable" in trend_status:
            return self.config.INTERPRETATION_STABLE.format(**params)
        else:
            return self.config.INTERPRETATION_DECLINING.format(**params)

    def render_welcome_message(self):
        """Render welcome message when no gene is selected."""
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.markdown(self.config.WELCOME_TITLE)
            st.markdown(self.config.WELCOME_TEXT)

    def render_results(
        self, gene_data: Dict, selected_genes: List[str], gene_history: Dict[str, dict]
    ):
        """
        Render complete results section.

        Args:
            gene_data: Current gene data
            selected_genes: Selected genes for comparison
            gene_history: All gene history
        """
        gene = gene_data["gene"]
        stats = gene_data["stats"]
        trend_status = gene_data["trend_status"]

        st.divider()

        # Results header and metrics
        st.subheader(self.config.SECTION_RESULTS_TITLE.format(gene=gene))
        self.render_metrics(stats)

        # Trend status
        self.render_trend_status(trend_status)

        st.divider()

        # Timeline chart
        self.render_timeline_chart(stats["years"], stats["counts"], gene)

        # Multi-gene comparison
        self.render_multi_gene_comparison(selected_genes, gene_history)

        # Additional charts
        self.render_additional_charts(stats)

        # Interpretation
        self.render_interpretation(stats, trend_status)
