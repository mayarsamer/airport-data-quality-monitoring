import sqlite3
import pandas as pd
from analysis_tools import load_data, analyze_missing_values, detect_flight_duration_outliers, detect_exact_duplicates, detect_duplicate_flight_numbers

def main():

    db_path = "../data/airport_data.db"
    table_name = "MOCK_DATA"
    df = load_data(db_path, table_name)


    missing_summary = analyze_missing_values(df, threshold=10.0)


    outlier_summary, detailed_outliers = detect_flight_duration_outliers(df)


    duplicated_rows = detect_exact_duplicates(df)

    duplicated_flight_number = detect_duplicate_flight_numbers(df)


#---------------------------------------------------------------------------------------------------------

    # Compose a Markdown report string combining all analysis outputs
    md_report = f"""
    # Analysis Report

    ## Missing Values Summary
    {missing_summary.to_markdown(index=False)}
  
    
  
    



    ## Flight Duration Outliers
    {outlier_summary.to_markdown(index=False)}

    

    



    ## Flight Duration Outliers (Detailed)
    {detailed_outliers.head(5).to_markdown(index=False)}

    

    



    ## Exact Duplicate Rows
    {duplicated_rows.to_markdown(index=False)}

    





       ## Duplicate Flight Numbers
    {duplicated_flight_number.head(20).to_markdown(index=False)}





    """

    # Write the Markdown report 
    with open("data_quality_report.md", "w") as f:
        f.write(md_report)

    print("Report saved to data_quality_report.md")

if __name__ == "__main__":
    main()
