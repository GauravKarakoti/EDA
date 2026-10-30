import pandas as pd

def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Clean known quality issues and return the cleaned frame plus audit metadata."""
    data = df.copy()
    audit = {"rows_before": len(data), "duplicates_removed": int(data.duplicated().sum())}

    data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
    data = data.drop_duplicates().copy()

    for col in ["region", "payment_method"]:
        if data[col].isna().any():
            mode = data[col].mode(dropna=True)
            fill_value = mode.iloc[0] if not mode.empty else "Unknown"
            data[col] = data[col].fillna(fill_value)

    if data["discount"].isna().any():
        data["discount"] = data["discount"].fillna(data["discount"].median())

    # Keep extreme values visible; flag for investigation instead of deleting blindly.
    quantity_cutoff = data["quantity"].quantile(0.99)
    data["quantity_outlier_flag"] = data["quantity"] > quantity_cutoff

    # Derive consistent analysis metrics.
    data["net_sales"] = (data["unit_price"] * data["quantity"] * (1 - data["discount"])).round(2)
    data["profit_margin"] = (data["profit"] / data["sales"].replace(0, pd.NA)).round(4)

    audit.update({
        "rows_after": len(data),
        "missing_values_after": int(data.isna().sum().sum()),
        "quantity_99th_percentile": float(quantity_cutoff),
        "quantity_outliers_flagged": int(data["quantity_outlier_flag"].sum())
    })
    return data, audit
