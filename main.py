from pathlib import Path
import html
import pandas as pd
from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.analysis import build_analysis
from src.visualization import create_figures

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "retail_transactions.csv"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

def money(value):
    return f"₹{value:,.2f}"

def main():
    raw = load_data(RAW)
    cleaned, audit = clean_data(raw)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED / "cleaned_retail_transactions.csv", index=False)

    analysis = build_analysis(cleaned)
    create_figures(cleaned, analysis, FIGURES)
    k = analysis["kpis"]

    top_category = analysis["category"].iloc[0]
    top_region = analysis["region"].iloc[0]
    monthly = analysis["monthly"]
    best_month = monthly.loc[monthly["revenue"].idxmax()] if not monthly.empty else None

    images = [
        ("Monthly Revenue Trend", "monthly_revenue.png"),
        ("Revenue by Category", "revenue_by_category.png"),
        ("Revenue by Region", "revenue_by_region.png"),
        ("Order Sales Distribution", "sales_distribution.png"),
        ("Numeric Correlation Heatmap", "correlation_heatmap.png"),
        ("Quantity Outlier Review", "quantity_boxplot.png")
    ]
    image_html = "".join(
        f'<section><h2>{title}</h2><img src="figures/{filename}" alt="{title}"></section>'
        for title, filename in images
    )
    report = f"""<!doctype html><html><head><meta charset="utf-8"><title>Retail EDA Report</title>
    <style>body{{font-family:Arial,sans-serif;max-width:1050px;margin:40px auto;padding:0 20px;color:#222}}
    h1,h2{{color:#17365d}}.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}
    .kpi{{background:#f2f5f9;padding:16px;border-radius:8px}}.value{{font-size:1.35rem;font-weight:bold}}
    img{{width:100%;height:auto;border:1px solid #ddd;border-radius:6px}}table{{border-collapse:collapse;width:100%}}
    td,th{{padding:9px;border-bottom:1px solid #ddd;text-align:left}}</style></head><body>
    <h1>Retail Transactions - Exploratory Data Analysis</h1>
    <p>Generated from a synthetic teaching dataset. Currency is illustrative (₹); results are not real business performance.</p>
    <div class="kpis">
      <div class="kpi">Transactions<div class="value">{k['transactions']:,}</div></div>
      <div class="kpi">Customers<div class="value">{k['customers']:,}</div></div>
      <div class="kpi">Revenue<div class="value">{money(k['revenue'])}</div></div>
      <div class="kpi">Profit<div class="value">{money(k['profit'])}</div></div>
      <div class="kpi">Average order value<div class="value">{money(k['avg_order_value'])}</div></div>
      <div class="kpi">Overall profit margin<div class="value">{k['overall_margin']:.1%}</div></div>
    </div>
    <h2>Data quality audit</h2>
    <table><tr><th>Metric</th><th>Result</th></tr>
    <tr><td>Raw rows</td><td>{audit['rows_before']}</td></tr>
    <tr><td>Exact duplicates removed</td><td>{audit['duplicates_removed']}</td></tr>
    <tr><td>Rows after cleaning</td><td>{audit['rows_after']}</td></tr>
    <tr><td>Missing values after cleaning</td><td>{audit['missing_values_after']}</td></tr>
    <tr><td>Quantity outliers flagged</td><td>{audit['quantity_outliers_flagged']}</td></tr></table>
    <h2>Key findings</h2><ul>
    <li>Highest-revenue category: <b>{html.escape(str(top_category['category']))}</b> ({money(top_category['revenue'])}).</li>
    <li>Highest-revenue region: <b>{html.escape(str(top_region['region']))}</b> ({money(top_region['revenue'])}).</li>
    <li>Overall profit margin: <b>{k['overall_margin']:.1%}</b>.</li>
    {"<li>Highest-revenue month: <b>" + html.escape(str(best_month['month'])) + "</b> (" + money(best_month['revenue']) + ").</li>" if best_month is not None else ""}
    </ul>
    <h2>Category summary</h2>{analysis['category'].to_html(index=False, float_format=lambda x: f"{x:,.2f}")}
    <h2>Regional summary</h2>{analysis['region'].to_html(index=False, float_format=lambda x: f"{x:,.2f}")}
    {image_html}
    <h2>Interpretation and limitations</h2>
    <p>This report is descriptive, not causal. The sample data is synthetically generated and contains designed data-quality issues.
    Outliers are flagged for investigation rather than automatically deleted. Before using similar methods on real data,
    validate business definitions (especially revenue, cost, discounts, returns, and tax treatment) with the data owner.</p>
    </body></html>"""
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "eda_report.html").write_text(report, encoding="utf-8")
    print("EDA complete.")
    print(f"Cleaned data: {PROCESSED / 'cleaned_retail_transactions.csv'}")
    print(f"HTML report: {REPORTS / 'eda_report.html'}")
    print(f"Figures: {FIGURES}")

if __name__ == "__main__":
    main()
