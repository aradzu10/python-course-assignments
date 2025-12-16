from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_penguins_data(file_path: str = "penguins.csv") -> pd.DataFrame:
    if Path(file_path).exists():
        return pd.read_csv(file_path, index_col="id")

    import kagglehub
    from kagglehub import KaggleDatasetAdapter

    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "ranaghulamnabi/penguins",
        "penguins.csv",
        pandas_kwargs=dict(index_col="id"),
    )
    df.to_csv(file_path, index=False)
    return df


def plot_null_values(df: pd.DataFrame, plot_dir: Path) -> None:
    plt.figure(figsize=(10, 6))

    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0]

    if len(null_counts) == 0:
        null_counts = df.isnull().sum()

    null_counts.plot(kind="barh", color="steelblue")
    plt.xlabel("Number of Missing Values")
    plt.ylabel("Column")
    plt.title("Missing Values per Column")
    plt.tight_layout()

    output_path = plot_dir / "01_null_values.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_column_distributions(df: pd.DataFrame, plot_dir: Path) -> None:
    numeric_cols = df.select_dtypes(include=["number"]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    total_cols = len(numeric_cols) + len(categorical_cols)

    fig, axes = plt.subplots(
        nrows=(total_cols + 2) // 3, ncols=3, figsize=(15, 5 * ((total_cols + 2) // 3))
    )
    axes = axes.flatten()

    idx = 0

    # Plot numeric columns as histograms
    for col in numeric_cols:
        axes[idx].hist(df[col].dropna(), bins=30, color="steelblue", edgecolor="black")
        axes[idx].set_title(f"{col} (Numeric)")
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel("Frequency")
        idx += 1

    # Plot categorical columns as bar charts
    for col in categorical_cols:
        df[col].value_counts().plot(
            kind="bar", ax=axes[idx], color="coral", edgecolor="black"
        )
        axes[idx].set_title(f"{col} (Categorical)")
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel("Count")
        axes[idx].tick_params(axis="x", rotation=45)
        idx += 1

    # Hide unused subplots
    for j in range(idx, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    output_path = plot_dir / "02_column_distributions.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_pairplot_by_species(df: pd.DataFrame, plot_dir: Path) -> None:
    plt.figure()

    pairplot = sns.pairplot(df, hue="species", plot_kws={"alpha": 0.6})
    pairplot.figure.suptitle("Pair Plot - Colored by Species", y=1.001)

    output_path = plot_dir / "03_pairplot_species.png"
    pairplot.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_pairplot_by_island(df: pd.DataFrame, plot_dir: Path) -> None:
    plt.figure()

    pairplot = sns.pairplot(df, hue="island", plot_kws={"alpha": 0.6})
    pairplot.figure.suptitle("Pair Plot - Colored by Island", y=1.001)

    output_path = plot_dir / "04_pairplot_island.png"
    pairplot.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_correlation_heatmap(df: pd.DataFrame, plot_dir: Path) -> None:
    numeric_df = df.select_dtypes(include=["number"])

    plt.figure(figsize=(10, 8))
    correlation_matrix = numeric_df.corr()

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        center=0,
        fmt=".2f",
        square=True,
        linewidths=0.5,
        cbar_kws={"label": "Correlation"},
    )
    plt.title("Correlation Heatmap - Numeric Features")
    plt.tight_layout()

    output_path = plot_dir / "05_correlation_heatmap.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_species_island_correlation(df: pd.DataFrame, plot_dir: Path) -> None:
    species_island_crosstab = pd.crosstab(df["species"], df["island"])

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        species_island_crosstab,
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        cbar_kws={"label": "Count"},
        linewidths=0.5,
    )
    plt.title("Species vs Island Distribution")
    plt.xlabel("Island")
    plt.ylabel("Species")
    plt.tight_layout()

    output_path = plot_dir / "06_species_island_correlation.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def main():
    print("Starting Penguins Data Analysis\n")

    df = load_penguins_data()
    print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")


    plot_dir = Path("plots")
    plot_dir.mkdir(exist_ok=True)
    print(f"Saving plots to: {plot_dir.resolve()}\n")

    # Generate all plots
    plots = {
        "Null Values": plot_null_values,
        "Column Distributions": plot_column_distributions,
        "Pair Plot by Species": plot_pairplot_by_species,
        "Pair Plot by Island": plot_pairplot_by_island,
        "Correlation Heatmap": plot_correlation_heatmap,
        "Species-Island Correlation": plot_species_island_correlation,
    }
    print(f"Generating {len(plots)} visualizations:")
    for i, (name, plot_func) in enumerate(plots.items(), 1):
        plot_func(df, plot_dir)
        print(f"{i}. Saved: {name}")
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
