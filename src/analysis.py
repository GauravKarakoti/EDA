import pandas as pd

def build_analysis(data: pd.DataFrame) -> dict:
    """Calculate business-facing summaries used in the report."""
    monthly = (data.assign(month=data["order_date"].dt.to_period("M").astype(str))
               .groupby("month", as_index=False)
               .agg(revenue=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")))
    category = (data.groupby("category", as_index=False)
                .agg(revenue=("sales", "sum"), profit=("profit", "sum"), quantity=("quantity", "sum"))
                .sort_values("revenue", ascending=False))
    region = (data.groupby("region", as_index=False)
              .agg(revenue=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
              .sort_values("revenue", ascending=False))
    payment = data["payment_method"].value_counts().rename_axis("payment_method").reset_index(name="transactions")
    customer = data.groupby("customer_id").agg(orders=("order_id", "nunique"), revenue=("sales", "sum"))
    return {
        "monthly": monthly, "category": category, "region": region, "payment": payment,
        "customer": customer,
        "kpis": {
            "transactions": int(data["order_id"].nunique()),
            "customers": int(data["customer_id"].nunique()),
            "revenue": float(data["sales"].sum()),
            "profit": float(data["profit"].sum()),
            "avg_order_value": float(data["sales"].sum() / max(data["order_id"].nunique(), 1)),
            "overall_margin": float(data["profit"].sum() / max(data["sales"].sum(), 1))
        }
    }
