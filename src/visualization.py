from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def create_figures(data, analysis, output_dir: str | Path):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(analysis["monthly"]["month"], analysis["monthly"]["revenue"], marker="o")
    ax.set(title="Monthly Revenue Trend", xlabel="Month", ylabel="Revenue")
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout(); fig.savefig(output_dir / "monthly_revenue.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    cat = analysis["category"].sort_values("revenue")
    ax.barh(cat["category"], cat["revenue"])
    ax.set(title="Revenue by Product Category", xlabel="Revenue", ylabel="Category")
    fig.tight_layout(); fig.savefig(output_dir / "revenue_by_category.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    reg = analysis["region"].sort_values("revenue")
    ax.bar(reg["region"], reg["revenue"])
    ax.set(title="Revenue by Region", xlabel="Region", ylabel="Revenue")
    fig.tight_layout(); fig.savefig(output_dir / "revenue_by_region.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(data["sales"].dropna(), bins=40)
    ax.set(title="Order Sales Distribution", xlabel="Sales", ylabel="Frequency")
    fig.tight_layout(); fig.savefig(output_dir / "sales_distribution.png", dpi=160); plt.close(fig)

    numeric = data.select_dtypes(include="number").select_dtypes(exclude="bool")
    corr = numeric.corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(corr, aspect="auto", cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=70, ha="right")
    ax.set_yticks(range(len(corr.columns)), corr.columns)
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="Correlation")
    ax.set_title("Numeric Feature Correlation")
    fig.tight_layout(); fig.savefig(output_dir / "correlation_heatmap.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.boxplot(data["quantity"].dropna(), vert=False)
    ax.set(title="Quantity Outlier Review", xlabel="Quantity")
    fig.tight_layout(); fig.savefig(output_dir / "quantity_boxplot.png", dpi=160); plt.close(fig)
