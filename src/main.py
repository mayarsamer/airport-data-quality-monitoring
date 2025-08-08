import sqlite3
import pandas as pd
from analysis_tools import load_data, analyze_missing_values, detect_outliers

def main():

    db_path = "airport_data.db"

    table_name = "MOCK_DATA"

    df = load_data(db_path, table_name)

    missing_summary = analyze_missing_values(df, threshold=10.0)

    outlier_summary, outlier_rows = detect_outliers(df, numeric_columns=None, threshold=1.5)

#---------------------------------------------------------------------------------------------------------

    md_report = f"""
    # Analysis Report

    ## Missing Values Summary
    {missing_summary.to_markdown()}

    ## Outlier Summary
    {outlier_summary.to_markdown()}
    """

    # Save or print
    with open("report.md", "w") as f:
        f.write(md_report)

    print("Report saved to report.md")

if __name__ == "__main__":
    main()
