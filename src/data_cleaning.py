"""
data_cleaning.py

Purpose: Load a messy sales CSV, apply standard cleaning steps, and write a cleaned CSV.
This script standardizes column names, trims whitespace, handles missing values,
and removes rows with invalid numeric values (negative price/quantity).
"""

from typing import Optional
import re
import pandas as pd


# Copilot-assisted function (generated suggestion reviewed & modified):
# Load the CSV file into a pandas DataFrame. Keep original raw text so we can fix types.
def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV from file_path into a pandas DataFrame.

    We explicitly do not coerce types here because the raw file has malformed values
    (currency symbols, 'N/A', empty strings). We'll clean types later.
    """
    df = pd.read_csv(file_path, dtype=str)
    return df


# Copilot-assisted function (generated suggestion reviewed & modified):
# Standardize column names to lowercase with underscores and strip leading/trailing whitespace
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and strip whitespace from string columns.

    This makes subsequent code simpler and consistent across datasets.
    """
    # Standardize column names
    df = df.rename(columns=lambda c: re.sub(r"\s+", "_", c.strip().lower()))

    # Strip whitespace from object/string columns for product/category-like fields
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()

    return df


def _to_numeric_clean(series: pd.Series, remove_currency: bool = True) -> pd.Series:
    """Helper: clean a numeric-ish series then convert to float where possible."""
    s = series.astype(str).str.strip()
    if remove_currency:
        s = s.str.replace(r"[^0-9.\-]", "", regex=True)
    s = s.replace({"": None, "nan": None, "None": None, "N/A": None, "NA": None})
    return pd.to_numeric(s, errors="coerce")


# Copilot-assisted function (generated suggestion reviewed & modified):
# Handle missing prices and quantities in a consistent way.
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill or drop missing values for price and quantity.

    Strategy used:
    - Convert `price` and `quantity` to numeric (coerce invalid to NaN).
    - Fill missing `quantity` with 1 (assume single unit when not provided).
    - Fill missing `price` with median price (robust to outliers).
    """
    # Clean numeric-like columns
    if "price" in df.columns:
        df["price"] = _to_numeric_clean(df["price"], remove_currency=True)
    else:
        df["price"] = pd.NA

    if "quantity" in df.columns:
        df["quantity"] = _to_numeric_clean(df["quantity"], remove_currency=False)
    else:
        df["quantity"] = pd.NA

    # Fill quantity missing with 1 (consistent choice)
    df["quantity"] = df["quantity"].fillna(1).astype(int)

    # Fill price missing with median price
    median_price: Optional[float] = None
    if df["price"].notna().any():
        median_price = df["price"].median()
        df["price"] = df["price"].fillna(median_price)
    else:
        # If no valid prices at all, fill with 0 to allow later filtering
        df["price"] = df["price"].fillna(0.0)

    return df


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with negative or zero price/quantity and other invalid cases.

    Rationale: Negative prices/quantities are likely data entry errors for a sales dataset.
    """
    # Remove rows where price or quantity is NaN (should be handled earlier, but double-check)
    df = df[df["price"].notna() & df["quantity"].notna()].copy()

    # Remove negative or zero price/quantity
    df = df[(df["price"] > 0) & (df["quantity"] > 0)]

    # Optionally drop rows that have no product or category
    if "product" in df.columns:
        df = df[~df["product"].isna() & (df["product"].str.strip() != "")]

    return df.reset_index(drop=True)


if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    # Load raw data
    df_raw = load_data(raw_path)

    # Normalize column names and strip whitespace
    df_clean = clean_column_names(df_raw)

    # Handle missing/invalid values consistently
    df_clean = handle_missing_values(df_clean)

    # Remove rows with clearly invalid numeric values
    df_clean = remove_invalid_rows(df_clean)

    # Ensure output dir exists
    import os

    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)

    # Write cleaned CSV
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())
