import pandas as pd
from src.data_cleaning import clean_column_names, handle_missing_values, remove_invalid_rows


def test_negative_values_removed_and_missing_filled():
    # Create a small dataframe that mimics raw input
    df = pd.DataFrame({
        "Product ": ["Good", "BadPrice", "NoQty"],
        " Price": ["$10.00", "-5.00", "12.00"],
        "Quantity ": ["2", "1", ""],
    })

    df = clean_column_names(df)
    df = handle_missing_values(df)
    df = remove_invalid_rows(df)

    # Ensure no non-positive prices or quantities remain
    assert (df["price"] > 0).all()
    assert (df["quantity"] > 0).all()


def test_missing_quantity_defaults_to_one():
    df = pd.DataFrame({"Product": ["X"], "Price": ["5"], "Quantity": [""]})
    df = clean_column_names(df)
    df = handle_missing_values(df)
    # After handling missing values, missing quantity should be filled with 1
    assert int(df.loc[0, "quantity"]) == 1
