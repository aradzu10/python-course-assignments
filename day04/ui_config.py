"""
UI configuration and text content for the Gene Trend Tracker application.
"""


class UIConfig:
    """UI configuration and text content."""

    # Page configuration
    PAGE_TITLE = "Gene Trend Tracker"
    PAGE_ICON = "🧬"
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"

    # Header texts
    MAIN_HEADER = "🧬 Gene Trend Tracker"
    SUB_HEADER = (
        "Discover if a gene is a hot topic or old news based on publication trends"
    )

    # Sidebar content
    SIDEBAR_ABOUT_TITLE = "📖 About"
    SIDEBAR_ABOUT_TEXT = """
This dashboard analyzes research activity for specific genes by tracking
publication counts in PubMed over the last 20 years.
"""

    SIDEBAR_HOW_TO_TITLE = "🔍 How to Use"
    SIDEBAR_HOW_TO_TEXT = """
1. Enter a gene or topic name
2. Click "Track Trend"
3. Analyze the visualizations and metrics
"""

    SIDEBAR_EXAMPLES_TITLE = "💡 Example Genes or Topics"
    EXAMPLE_GENES = ["TP53", "BRCA1", "EGFR", "APOE", "ACE2", "MYC", "KRAS"]

    SIDEBAR_SETTINGS_TITLE = "⚙️ Settings"
    SETTING_USE_CACHE_LABEL = "Use cached data"
    SETTING_USE_CACHE_HELP = "Load data from cache if available (faster)"
    SETTING_CACHE_AGE_LABEL = "Cache age (days)"
    SETTING_CACHE_AGE_HELP = "Maximum age of cached data to use"
    BUTTON_CLEAR_CACHE = "Clear Cache"
    MESSAGE_CACHE_CLEARED = "Cache cleared!"

    # Input section
    INPUT_GENE_LABEL = "Gene or Topic Name"
    INPUT_GENE_PLACEHOLDER = "e.g., TP53, BRCA1, EGFR, CRISPR"
    INPUT_GENE_HELP = "Enter a gene name or research topic to analyze"
    BUTTON_TRACK_GENE = "🔍 Track Trend"

    # Multi-gene comparison
    SECTION_COMPARISON_TITLE = "📊 Compare Multiple Genes/Topics"
    MULTISELECT_LABEL = "Select genes or topics to compare"
    MULTISELECT_HELP = "Select multiple items to overlay on the same chart"
    BUTTON_CLEAR_HISTORY = "🗑️ Clear History"

    # Status messages
    MESSAGE_ENTER_GENE = "❌ Please enter a gene or topic name."
    MESSAGE_CACHED = "📦 Loaded from cache"
    MESSAGE_VALIDATING = "Validating '{gene}'..."
    MESSAGE_VALIDATION_FAILED = (
        "❌ No publications found for '{gene}'. Please check the name and try again."
    )
    MESSAGE_VALIDATED = "✅ '{gene}' validated!"
    MESSAGE_FETCHING = "Fetching data for {gene}..."
    MESSAGE_FETCHING_PROGRESS = (
        "Fetching {gene} data: {year} ({completed}/{total} years)"
    )
    MESSAGE_FETCH_COMPLETE = "✅ Data fetch complete!"
    MESSAGE_ERROR = "❌ Error processing data: {error}"
    MESSAGE_YEAR_COUNT = "Year {year}: {count} publications"

    # Results section
    SECTION_RESULTS_TITLE = "📊 Analysis Results for {gene}"
    METRIC_TOTAL_LABEL = "Total Publications"
    METRIC_AVERAGE_LABEL = "Average per Year"
    METRIC_PEAK_LABEL = "Peak Year"
    METRIC_RECENT_LABEL = "Recent 5-Year Total"

    SECTION_TREND_STATUS = "### 🎯 Trend Status"
    SECTION_TIMELINE = "📈 Publication Timeline"
    SECTION_MULTI_GENE = "🔬 Multi-Topic Comparison"
    SECTION_COMPARISON_SUMMARY = "📊 Comparison Summary"
    SECTION_GROWTH_INDICATOR = "📊 Growth Indicator"
    SECTION_YOY_GROWTH = "🔄 Year-over-Year Growth"
    SECTION_ACTIVITY_COMPARISON = "⚖️ Activity Comparison"
    SECTION_INTERPRETATION = "💡 Interpretation"

    # Comparison table columns
    TABLE_COL_GENE = "Gene or Topic"
    TABLE_COL_TOTAL = "Total Publications"
    TABLE_COL_AVERAGE = "Avg/Year"
    TABLE_COL_PEAK = "Peak Year"
    TABLE_COL_TREND = "Recent Trend"
    TABLE_COL_STATUS = "Status"

    # Welcome message
    WELCOME_TITLE = "### 👋 Welcome to Gene Trend Tracker!"
    WELCOME_TEXT = """
Enter a gene or topic name above to get started, or try one of the examples from the sidebar.

#### What you'll discover:
- 📊 **Publication timeline** over 20 years
- 📈 **Trend analysis** with growth metrics
- 🎯 **Trend status** (Hot Topic, Growing, Stable, or Declining)
- 💡 **Insights** about research activity

#### Popular genes or topics to explore:
- **TP53** - The "guardian of the genome"
- **BRCA1** - Breast cancer susceptibility gene
- **EGFR** - Cancer therapy target
- **APOE** - Alzheimer's disease related
- **ACE2** - COVID-19 receptor
"""

    # Trend status labels
    STATUS_HOT = "🔥 Hot Topic"
    STATUS_GROWING = "📈 Growing"
    STATUS_STABLE = "📊 Stable"
    STATUS_DECLINING = "📉 Declining"

    # Interpretation templates
    INTERPRETATION_HOT = """
🔥 **{total:,}** total publications with a **{trend:+.1f}%** increase in recent activity! 
This topic is experiencing significant research growth and is currently a hot topic in the scientific community.
Publications peaked in **{peak_year}** with **{peak_count:,}** papers.
"""

    INTERPRETATION_GROWING = """
📈 **{total:,}** total publications with a **{trend:+.1f}%** increase in recent activity.
This topic is gaining attention in research circles. Publications peaked in **{peak_year}** 
with **{peak_count:,}** papers.
"""

    INTERPRETATION_STABLE = """
📊 **{total:,}** total publications with relatively stable activity (**{trend:+.1f}%** change).
This topic maintains consistent research interest. Publications peaked in **{peak_year}** 
with **{peak_count:,}** papers.
"""

    INTERPRETATION_DECLINING = """
📉 **{total:,}** total publications with a **{trend:.1f}%** decrease in recent activity.
Research interest in this topic has declined compared to previous years. Publications peaked in **{peak_year}** 
with **{peak_count:,}** papers.
"""

    # CSS styles
    CUSTOM_CSS = """
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f1f1f;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4B8BFF;
    }
    .status-hot {
        color: #FF4B4B;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .status-growing {
        color: #FFA500;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .status-stable {
        color: #4B8BFF;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .status-declining {
        color: #808080;
        font-weight: bold;
        font-size: 1.5rem;
    }
    </style>
"""

    # Color scheme
    COLORS = {
        "hot": "#FF4B4B",
        "growing": "#FFA500",
        "stable": "#4B8BFF",
        "declining": "#808080",
    }

    MULTI_GENE_COLORS = [
        "#FF4B4B",  # Red
        "#4B8BFF",  # Blue
        "#4CAF50",  # Green
        "#FFA500",  # Orange
        "#9C27B0",  # Purple
        "#00BCD4",  # Cyan
        "#FF9800",  # Deep Orange
        "#E91E63",  # Pink
    ]
