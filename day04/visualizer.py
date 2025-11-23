"""
Visualizer for Gene Trend Tracker.

Creates charts and visualizations for publication trends.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import numpy as np
from ui_config import UIConfig


class TrendVisualizer:
    """Create visualizations for gene publication trends."""

    def __init__(self):
        """Initialize the visualizer."""
        self.color_scheme = UIConfig.COLORS

    def create_timeline_chart(
        self, years: List[int], counts: List[int], gene: str
    ) -> go.Figure:
        """
        Create an interactive timeline chart of publication counts.

        Args:
            years: List of years
            counts: List of publication counts
            gene: Gene name for title

        Returns:
            Plotly figure object
        """
        # Calculate trend line
        if len(years) > 1:
            z = np.polyfit(years, counts, 2)  # Quadratic fit
            p = np.poly1d(z)
            trend_y = p(years)
        else:
            trend_y = counts

        # Create figure
        fig = go.Figure()

        # Add bar chart for actual counts
        fig.add_trace(
            go.Bar(
                x=years,
                y=counts,
                name="Publications",
                marker_color="#4B8BFF",
                hovertemplate="<b>Year:</b> %{x}<br>"
                + "<b>Publications:</b> %{y}<br>"
                + "<extra></extra>",
            )
        )

        # Add trend line
        fig.add_trace(
            go.Scatter(
                x=years,
                y=trend_y,
                name="Trend",
                line=dict(color="#FF4B4B", width=3, dash="dash"),
                hovertemplate="<b>Trend:</b> %{y:.0f}<br><extra></extra>",
            )
        )

        # Update layout
        fig.update_layout(
            title=dict(
                text=f"Publication Trend for {gene}",
                font=dict(size=24, color="#1f1f1f"),
            ),
            xaxis_title="Year",
            yaxis_title="Number of Publications",
            hovermode="x unified",
            template="plotly_white",
            showlegend=True,
            height=500,
            font=dict(size=12),
            plot_bgcolor="rgba(240,240,240,0.5)",
        )

        fig.update_xaxes(
            tickmode="linear",
            tick0=min(years),
            dtick=2,
            gridcolor="rgba(200,200,200,0.3)",
        )

        fig.update_yaxes(gridcolor="rgba(200,200,200,0.3)")

        return fig

    def create_recent_comparison_chart(
        self, recent_5: int, previous_5: int
    ) -> go.Figure:
        """
        Create a comparison chart for recent vs previous 5-year periods.

        Args:
            recent_5: Publication count for recent 5 years
            previous_5: Publication count for previous 5 years

        Returns:
            Plotly figure object
        """
        categories = ["Previous 5 Years", "Recent 5 Years"]
        values = [previous_5, recent_5]
        colors = ["#808080", "#FF4B4B"]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=categories,
                    y=values,
                    marker_color=colors,
                    text=values,
                    textposition="auto",
                    hovertemplate="<b>%{x}</b><br>"
                    + "Publications: %{y}<br>"
                    + "<extra></extra>",
                )
            ]
        )

        fig.update_layout(
            title="5-Year Activity Comparison",
            yaxis_title="Number of Publications",
            template="plotly_white",
            height=300,
            showlegend=False,
        )

        return fig

    def create_growth_indicator(self, trend_change_percent: float) -> go.Figure:
        """
        Create a gauge chart showing growth rate.

        Args:
            trend_change_percent: Percentage change in trend

        Returns:
            Plotly figure object
        """
        # Determine color based on trend
        if trend_change_percent > 50:
            color = "#FF4B4B"
        elif trend_change_percent > 10:
            color = "#FFA500"
        elif trend_change_percent > -10:
            color = "#4B8BFF"
        else:
            color = "#808080"

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=trend_change_percent,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Trend Change", "font": {"size": 20}},
                delta={"reference": 0, "suffix": "%"},
                number={"suffix": "%"},
                gauge={
                    "axis": {
                        "range": [-100, 100],
                        "tickwidth": 1,
                        "tickcolor": "darkgray",
                    },
                    "bar": {"color": color},
                    "bgcolor": "white",
                    "borderwidth": 2,
                    "bordercolor": "gray",
                    "steps": [
                        {"range": [-100, -10], "color": "rgba(128,128,128,0.2)"},
                        {"range": [-10, 10], "color": "rgba(75,139,255,0.2)"},
                        {"range": [10, 50], "color": "rgba(255,165,0,0.2)"},
                        {"range": [50, 100], "color": "rgba(255,75,75,0.2)"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": trend_change_percent,
                    },
                },
            )
        )

        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))

        return fig

    def create_yearly_growth_chart(
        self, years: List[int], counts: List[int]
    ) -> go.Figure:
        """
        Create a year-over-year growth rate chart.

        Args:
            years: List of years
            counts: List of publication counts

        Returns:
            Plotly figure object
        """
        if len(years) < 2:
            return go.Figure()

        # Calculate year-over-year growth
        growth_rates = []
        growth_years = []

        for i in range(1, len(counts)):
            if counts[i - 1] > 0:
                growth = ((counts[i] - counts[i - 1]) / counts[i - 1]) * 100
                growth_rates.append(growth)
                growth_years.append(years[i])

        # Color bars based on positive/negative growth
        colors = ["#4CAF50" if g >= 0 else "#FF5252" for g in growth_rates]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=growth_years,
                    y=growth_rates,
                    marker_color=colors,
                    hovertemplate="<b>Year:</b> %{x}<br>"
                    + "<b>Growth:</b> %{y:.1f}%<br>"
                    + "<extra></extra>",
                )
            ]
        )

        fig.update_layout(
            title="Year-over-Year Growth Rate",
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            template="plotly_white",
            height=300,
            showlegend=False,
        )

        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

        return fig

    def create_multi_gene_comparison(
        self, gene_data: Dict[str, Dict[str, List]]
    ) -> go.Figure:
        """
        Create an overlaid comparison chart for multiple genes.

        Args:
            gene_data: Dictionary mapping gene names to their data
                      Format: {gene_name: {"years": [...], "counts": [...]}}

        Returns:
            Plotly figure object
        """
        # Color palette for different genes
        colors = UIConfig.MULTI_GENE_COLORS

        fig = go.Figure()

        for idx, (gene, data) in enumerate(gene_data.items()):
            color = colors[idx % len(colors)]

            # Add line for each gene
            fig.add_trace(
                go.Scatter(
                    x=data["years"],
                    y=data["counts"],
                    name=gene,
                    mode="lines+markers",
                    line=dict(color=color, width=3),
                    marker=dict(size=6),
                    hovertemplate=f"<b>{gene}</b><br>"
                    + "<b>Year:</b> %{x}<br>"
                    + "<b>Publications:</b> %{y}<br>"
                    + "<extra></extra>",
                )
            )

        fig.update_layout(
            title=dict(
                text="Multi-Gene Publication Comparison",
                font=dict(size=24, color="#1f1f1f"),
            ),
            xaxis_title="Year",
            yaxis_title="Number of Publications",
            hovermode="x unified",
            template="plotly_white",
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            height=500,
            font=dict(size=12),
            plot_bgcolor="rgba(240,240,240,0.5)",
        )

        # Only update x-axis if there's data
        if gene_data:
            all_years = [
                year
                for data in gene_data.values()
                if data.get("years")
                for year in data["years"]
            ]
            if all_years:
                fig.update_xaxes(
                    tickmode="linear",
                    tick0=min(all_years),
                    dtick=2,
                    gridcolor="rgba(200,200,200,0.3)",
                )
        else:
            fig.update_xaxes(gridcolor="rgba(200,200,200,0.3)")

        fig.update_yaxes(gridcolor="rgba(200,200,200,0.3)")

        return fig


def main():
    """Example usage of the visualizer."""
    visualizer = TrendVisualizer()

    # Example data
    years = list(range(2004, 2025))
    counts = [
        1500,
        1600,
        1700,
        1800,
        1900,
        2000,
        2100,
        2200,
        2400,
        2600,
        2800,
        3000,
        3200,
        3400,
        3600,
        3900,
        4200,
        4500,
        4800,
        5100,
        5400,
    ]

    # Create timeline chart
    fig = visualizer.create_timeline_chart(years, counts, "TP53")
    fig.show()

    # Create comparison chart
    recent_5 = sum(counts[-5:])
    previous_5 = sum(counts[-10:-5])
    fig2 = visualizer.create_recent_comparison_chart(recent_5, previous_5)
    fig2.show()

    # Create growth indicator
    trend_change = ((recent_5 - previous_5) / previous_5) * 100
    fig3 = visualizer.create_growth_indicator(trend_change)
    fig3.show()

    # Create yearly growth chart
    fig4 = visualizer.create_yearly_growth_chart(years, counts)
    fig4.show()


if __name__ == "__main__":
    main()
