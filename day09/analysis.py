"""
Course Assignment Submission Analysis
=====================================

This module analyzes student submission patterns for course assignments.
Creates various visualizations to understand submission behavior.
"""

import warnings
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from adjustText import adjust_text

# Configure matplotlib for better plots
plt.style.use("default")
sns.set_palette("husl")
warnings.filterwarnings("ignore")

# Create plots directory if it doesn't exist
PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)


def load_and_parse_data():
    """Load all CSV files and parse dates correctly."""
    print("Loading and parsing data...")

    # Load assignments data
    assignments = pd.read_csv("data/assignments.csv")
    assignments["date_begin"] = pd.to_datetime(
        assignments["date_begin"], format="%Y.%m.%d %H:%M"
    )
    assignments["date_end"] = pd.to_datetime(
        assignments["date_end"], format="%Y.%m.%d %H:%M"
    )
    assignments["duration_days"] = (
        assignments["date_end"] - assignments["date_begin"]
    ).dt.total_seconds() / (24 * 3600)

    # Load submissions data
    subjects = pd.read_csv("data/subjects.csv")
    subjects["date"] = pd.to_datetime(subjects["date"]).dt.tz_localize(
        None
    )  # Remove timezone
    # subjects = subjects[
    #     subjects["assignment_name"] != "Proposal"
    # ]  # Filter out proposals

    # Load classes data
    classes = pd.read_csv("data/classes.csv")
    classes["date"] = pd.to_datetime(classes["date"], format="%d.%m.%Y %H:%M")

    # Merge submissions with assignment deadlines
    data = subjects.merge(assignments, on="assignment_name", how="left")
    data["hours_before_deadline"] = (
        data["date_end"] - data["date"]
    ).dt.total_seconds() / 3600
    data["submission_day"] = data["date"].dt.day_name()
    data["submission_hour"] = data["date"].dt.hour
    data["submission_weekday"] = data["date"].dt.weekday + 1  # 1=Monday, 7=Sunday
    data["submission_weekday"] = data["submission_weekday"].replace({7: 0})

    # Add time period categories
    def categorize_time(row):
        weekday = row["submission_weekday"]
        hour = row["submission_hour"]

        if weekday >= 6:  # Friday=6, Saturday=7
            return "Weekend"
        elif 9 <= hour <= 17:
            return "Weekday Working Hours"
        else:
            return "Weekday After Hours"

    data["time_category"] = data.apply(categorize_time, axis=1)

    print(
        f"Loaded {len(assignments)} assignments, {len(subjects)} submissions, {len(classes)} classes"
    )
    return data, assignments, subjects, classes


def plot_submission_heatmap(data):
    """Create submission heatmap by day of week and hour."""
    print("Creating submission heatmap...")

    # Create pivot table for heatmap
    heatmap_data = (
        data.groupby(["submission_weekday", "submission_hour"])
        .size()
        .unstack(fill_value=0)
    )

    # Create proper day labels
    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    plt.figure(figsize=(14, 8))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        cbar_kws={"label": "Number of Submissions"},
        yticklabels=day_labels,
    )

    plt.title("Submission Heatmap: Day of Week vs Hour of Day", fontsize=16, pad=20)
    plt.xlabel("Hour of Day (0-23)", fontsize=12)
    plt.ylabel("Day of Week", fontsize=12)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "submission_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_student_persona_scatter(data):
    """Create student persona scatter plot (earliness vs consistency)."""
    print("Creating student persona scatter plot...")

    # Calculate student statistics
    student_stats = (
        data.groupby("user")
        .agg({"hours_before_deadline": ["mean", "std", "count"]})
        .round(2)
    )

    student_stats.columns = ["mean_earliness", "consistency", "submission_count"]
    student_stats = student_stats.reset_index()
    student_stats["consistency"] = student_stats["consistency"].fillna(
        0
    )  # Handle single submissions

    # Filter students with at least 3 submissions for meaningful analysis
    frequent_students = student_stats[student_stats["submission_count"] >= 3]

    plt.figure(figsize=(12, 8))

    # Create scatter plot with point size based on submission count
    scatter = plt.scatter(
        frequent_students["mean_earliness"],
        frequent_students["consistency"],
        s=frequent_students["submission_count"] * 20,
        alpha=0.6,
        c=frequent_students["submission_count"],
        cmap="viridis",
    )

    plt.colorbar(scatter, label="Number of Submissions")

    # Add labels for interesting points using adjust_text
    for i, student in frequent_students.iterrows():
        plt.annotate(
            student["user"],
            (student["mean_earliness"], student["consistency"]),
            fontsize=8,
            alpha=0.8,
        )
    
    plt.xlabel("Mean Earliness (Hours Before Deadline)", fontsize=12)
    plt.ylabel("Consistency (Standard Deviation of Earliness)", fontsize=12)
    plt.title(
        "Student Personas: Earliness vs Consistency\n(Point size = number of submissions)",
        fontsize=14,
        pad=20,
    )
    plt.xscale("symlog")
    plt.yscale("log")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "student_persona_scatter.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_submission_velocity_ecdf(data):
    """Create ECDF plot showing submission velocity for each assignment."""
    print("Creating submission velocity ECDF plot...")

    plt.figure(figsize=(14, 8))

    assignments = data["assignment_name"].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(assignments)))
    deadline_annotations = []

    for i, assignment in enumerate(assignments):
        assignment_data = data[data["assignment_name"] == assignment]

        # Calculate time relative to deadline (negative = before, positive = after)
        relative_times = -assignment_data["hours_before_deadline"]
        relative_times_sorted = np.sort(relative_times)

        # Create ECDF
        n = len(relative_times_sorted)
        y = np.arange(1, n + 1) / n * 100

        plt.plot(
            relative_times_sorted,
            y,
            label=f"{assignment} (n={n})",
            linewidth=2.5,
            color=colors[i],
        )

        # Calculate percentage submitted by deadline
        submitted_by_deadline = (assignment_data["hours_before_deadline"] >= 0).sum()
        pct_by_deadline = (submitted_by_deadline / n) * 100

        # Find y-value at deadline (x=0)
        deadline_idx = np.searchsorted(relative_times_sorted, 0)
        if deadline_idx < len(y):
            deadline_y = y[deadline_idx] if deadline_idx < len(y) else y[-1]
        else:
            deadline_y = 100

        deadline_annotations.append(
            {
                "assignment": assignment,
                "pct": pct_by_deadline,
                "y": deadline_y,
                "color": colors[i],
            }
        )

    plt.axvline(x=0, color="red", linestyle="--", alpha=0.7, label="Deadline")

    # Sort annotations by y-value to prevent overlap
    deadline_annotations.sort(key=lambda x: x["y"])

    # Add annotations with manual spacing
    for i, ann in enumerate(deadline_annotations):
        # Position annotations alternating left and right of deadline
        x_offset = 50 if i % 2 == 0 else -50
        y_position = ann["y"]

        # Adjust y-position if too close to previous annotation
        if i > 0:
            prev_y = (
                deadline_annotations[i - 1]["y"]
                if i % 2 == 0
                else deadline_annotations[i - 1]["y"]
            )
            if abs(y_position - prev_y) < 8:  # Minimum spacing of 8%
                y_position = prev_y + 8 if i % 2 == 0 else prev_y - 8

        plt.annotate(
            f"{ann['pct']:.0f}%",
            (0, ann["y"]),
            xytext=(x_offset, 0),
            textcoords="offset points",
            fontsize=8,
            alpha=0.8,
            color=ann["color"],
            fontweight="bold",
            ha="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
            arrowprops=dict(arrowstyle="->", color=ann["color"], alpha=0.6),
        )

    plt.xlabel(
        "Hours Relative to Deadline (negative = early, positive = late)", fontsize=12
    )
    plt.ylabel("Cumulative Percentage of Submissions (%)", fontsize=12)
    plt.title(
        "Submission Velocity: Cumulative Distribution by Assignment",
        fontsize=14,
        pad=20,
    )
    plt.xscale("symlog")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        PLOTS_DIR / "submission_velocity_ecdf.png", dpi=300, bbox_inches="tight"
    )
    plt.close()


def plot_weekend_warrior_stacked_bar(data):
    """Create stacked bar chart showing submission time categories by assignment."""
    print("Creating weekend warrior stacked bar chart...")

    # Calculate proportions for each assignment
    time_props = (
        data.groupby(["assignment_name", "time_category"]).size().unstack(fill_value=0)
    )
    time_props_pct = time_props.div(time_props.sum(axis=1), axis=0) * 100

    plt.figure(figsize=(12, 8))

    # Define colors for each category
    colors = {
        "Weekday Working Hours": "#2E86AB",
        "Weekday After Hours": "#A23B72",
        "Weekend": "#F18F01",
    }

    # Create stacked bar chart
    bottom = np.zeros(len(time_props_pct))

    for category in ["Weekday Working Hours", "Weekday After Hours", "Weekend"]:
        if category in time_props_pct.columns:
            bars = plt.bar(
                time_props_pct.index,
                time_props_pct[category],
                bottom=bottom,
                label=category,
                color=colors[category],
            )

            # Add percentage labels on bars
            for i, (bar, pct) in enumerate(zip(bars, time_props_pct[category])):
                if pct > 5:  # Only show labels for segments > 5%
                    height = pct / 2  # Middle of the segment
                    plt.text(
                        bar.get_x() + bar.get_width() / 2.0,
                        bottom[i] + height,
                        f"{pct:.0f}%",
                        ha="center",
                        va="center",
                        fontsize=8,
                        fontweight="bold",
                        color="white",
                    )

            bottom += time_props_pct[category]

    plt.xlabel("Assignment", fontsize=12)
    plt.ylabel("Percentage of Submissions (%)", fontsize=12)
    plt.title(
        "Weekend Warrior Analysis: Submission Time Distribution by Assignment",
        fontsize=14,
        pad=20,
    )
    plt.legend()
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.savefig(
        PLOTS_DIR / "weekend_warrior_stacked_bar.png", dpi=300, bbox_inches="tight"
    )
    plt.close()


def analyze_time_allocation_patterns(data):
    """Analyze whether longer assignment time changes submission timing relative to deadline."""
    print("Analyzing time allocation patterns...")

    # Remove proposals from data
    data = data[data["assignment_name"] != "Proposal"]

    # Add relative timing calculations
    data["assignment_duration_hours"] = data["duration_days"] * 24
    data["time_from_start"] = (
        data["date"] - data["date_begin"]
    ).dt.total_seconds() / 3600
    data["relative_submission_time"] = (
        data["time_from_start"] / data["assignment_duration_hours"]
    ) * 100

    # Calculate patterns by assignment
    assignment_patterns = (
        data.groupby("assignment_name")
        .agg(
            {
                "hours_before_deadline": ["mean", "median", "std"],
                "duration_days": "first",
                "user": "count",
                "relative_submission_time": ["mean", "median", "std"],
            }
        )
        .round(2)
    )

    assignment_patterns.columns = [
        "mean_earliness_hours",
        "median_earliness_hours",
        "std_earliness_hours",
        "duration_days",
        "submission_count",
        "mean_relative_timing",
        "median_relative_timing",
        "std_relative_timing",
    ]
    assignment_patterns = assignment_patterns.reset_index()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    # Plot 1: Duration vs Relative Submission Timing
    scatter1 = ax1.scatter(
        assignment_patterns["duration_days"],
        assignment_patterns["mean_relative_timing"],
        s=assignment_patterns["submission_count"] * 5,
        alpha=0.7,
        c="blue",
    )

    # Add annotations for each assignment
    texts1 = []
    for i, row in assignment_patterns.iterrows():
        texts1.append(
            ax1.annotate(
                row["assignment_name"],
                (row["duration_days"], row["mean_relative_timing"]),
                fontsize=8,
                alpha=0.8,
            )
        )

    adjust_text(
        texts1, ax=ax1, arrowprops=dict(arrowstyle="-", color="gray", alpha=0.5)
    )

    ax1.axhline(
        y=90, color="red", linestyle="--", alpha=0.7, label="90% through assignment"
    )
    ax1.set_xlabel("Assignment Duration (Days)")
    ax1.set_ylabel("Mean Relative Timing (% through assignment)")
    ax1.set_title(
        "Do students submit at consistent relative times?\n(100% = deadline, 0% = assignment start)"
    )
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_ylim(0, 110)

    # Add correlation coefficient
    corr1 = np.corrcoef(
        assignment_patterns["duration_days"],
        assignment_patterns["mean_relative_timing"],
    )[0, 1]
    ax1.text(
        0.05,
        0.95,
        f"Correlation: {corr1:.3f}",
        transform=ax1.transAxes,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    # Plot 2: Duration vs Absolute Earliness
    scatter2 = ax2.scatter(
        assignment_patterns["duration_days"],
        assignment_patterns["mean_earliness_hours"],
        s=assignment_patterns["submission_count"] * 5,
        alpha=0.7,
        c="green",
    )

    # Add annotations for each assignment
    texts2 = []
    for i, row in assignment_patterns.iterrows():
        texts2.append(
            ax2.annotate(
                row["assignment_name"],
                (row["duration_days"], row["mean_earliness_hours"]),
                fontsize=8,
                alpha=0.8,
            )
        )

    adjust_text(
        texts2, ax=ax2, arrowprops=dict(arrowstyle="-", color="gray", alpha=0.5)
    )

    ax2.set_xlabel("Assignment Duration (Days)")
    ax2.set_ylabel("Mean Submission Earliness (Hours before deadline)")
    ax2.set_title(
        "Do longer assignments get earlier submissions?\n(Absolute time before deadline)"
    )
    ax2.grid(True, alpha=0.3)

    corr2 = np.corrcoef(
        assignment_patterns["duration_days"],
        assignment_patterns["mean_earliness_hours"],
    )[0, 1]
    ax2.text(
        0.05,
        0.95,
        f"Correlation: {corr2:.3f}",
        transform=ax2.transAxes,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    # Plot 3: Box plot of relative timing by assignment (sorted by duration)
    assignments_sorted = assignment_patterns.sort_values("duration_days")

    # Prepare data for boxplot
    boxplot_data = []
    labels = []
    for assignment in assignments_sorted["assignment_name"]:
        assignment_data = data[data["assignment_name"] == assignment][
            "relative_submission_time"
        ]
        boxplot_data.append(assignment_data)
        duration = assignment_patterns[
            assignment_patterns["assignment_name"] == assignment
        ]["duration_days"].iloc[0]
        labels.append(f"{assignment}\n({duration:.1f}d)")

    ax3.boxplot(boxplot_data, labels=labels)
    ax3.axhline(
        y=90, color="red", linestyle="--", alpha=0.7, label="90% through assignment"
    )
    ax3.set_ylabel("Relative Submission Time (% through assignment)")
    ax3.set_title("Distribution of submission timing\n(sorted by assignment duration)")
    ax3.tick_params(axis="x", rotation=45)
    ax3.grid(True, alpha=0.3, axis="y")
    ax3.legend()
    ax3.set_ylim(0, 110)

    plt.tight_layout()
    plt.savefig(
        PLOTS_DIR / "time_allocation_patterns.png", dpi=300, bbox_inches="tight"
    )
    plt.close()

    return assignment_patterns


def generate_summary_statistics(data, assignments, assignment_patterns):
    """Generate summary statistics for the analysis."""
    print("Generating summary statistics...")

    stats = {
        "total_assignments": len(assignments),
        "total_submissions": len(data),
        "unique_students": data["user"].nunique(),
        "avg_submissions_per_student": len(data) / data["user"].nunique(),
        "mean_earliness_hours": data["hours_before_deadline"].mean(),
        "median_earliness_hours": data["hours_before_deadline"].median(),
        "late_submissions_pct": (data["hours_before_deadline"] < 0).mean() * 100,
        "weekend_submissions_pct": (data["time_category"] == "Weekend").mean() * 100,
        "duration_earliness_correlation": np.corrcoef(
            assignment_patterns["duration_days"],
            assignment_patterns["mean_earliness_hours"],
        )[0, 1],
    }

    return stats


def main():
    """Main analysis function."""
    print("=== Course Assignment Submission Analysis ===\n")

    # Load and parse data
    data, assignments, subjects, classes = load_and_parse_data()

    # Generate all plots
    plot_submission_heatmap(data)
    plot_student_persona_scatter(data)
    plot_submission_velocity_ecdf(data)
    plot_weekend_warrior_stacked_bar(data)

    # Advanced analyses
    assignment_patterns = analyze_time_allocation_patterns(data)

    # Generate summary statistics
    stats = generate_summary_statistics(data, assignments, assignment_patterns)

    print("\n=== Analysis Complete ===")
    print(f"Generated 5 plots in {PLOTS_DIR}/")
    print(f"Total submissions analyzed: {stats['total_submissions']}")
    print(f"Students: {stats['unique_students']}")
    print(
        f"Mean submission earliness: {stats['mean_earliness_hours']:.1f} hours before deadline"
    )
    print(f"Late submissions: {stats['late_submissions_pct']:.1f}%")
    print(f"Weekend submissions: {stats['weekend_submissions_pct']:.1f}%")


if __name__ == "__main__":
    main()
