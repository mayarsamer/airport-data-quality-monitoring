import sqlite3
import pandas as pd
from analysis_tools import load_data, analyze_missing_values, detect_outliers

def main():
    # Example input values
    db_path = "airport_data.db"
    table_name = "MOCK_DATA"

    # Call load_data with actual arguments (without type annotations)
    df = load_data(db_path, table_name)
    print("Function1 output (dataframe head):")
    print(df.head())

    # Call analyze_missing_values with the dataframe and threshold value
    missing_summary = analyze_missing_values(df, threshold=10.0)
    print("\nFunction2 output (missing values summary):")
    print(missing_summary)

    # Call detect_outliers with the dataframe and optional arguments
    outlier_summary, outlier_rows = detect_outliers(df, numeric_columns=None, threshold=1.5)
    print("\nFunction3 output (outlier summary):")
    print(outlier_summary)
    print("\nOutlier rows:")
    print(outlier_rows)

if __name__ == "__main__":
    main()
