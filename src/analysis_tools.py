import sqlite3
import pandas as pd
import re

def load_data(db_path: str, table_name: str) -> pd.DataFrame:
    """Connect to the SQLite database and return the table as a DataFrame."""
    # Open a connection to the SQLite database file
    conn = sqlite3.connect(db_path)
    
    # Use pandas to run a SQL query that selects everything from the specified table
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    
    # Close the database connection to free resources
    conn.close()
    
    # Return the loaded data as a DataFrame for further analysis
    return df


#----------------------------------------------------------------------------------------


def analyze_missing_values(df: pd.DataFrame, threshold: float = 10.0):
    """
    Calculate the percentage of missing values in each column,
    and prepare a human-friendly summary with a highlight emoji if above threshold.
    """
    
    # Calculate missing data percentage per column (fraction * 100)
    missing_percentages = df.isnull().mean() * 100
    
    # Reset index to convert Series into a DataFrame with columns
    missing_summary = missing_percentages.reset_index()
    
    # Rename columns for clarity
    missing_summary.columns = ['Column', 'MissingPercentage']
    
    # Function to add a warning emoji if missing percentage is above threshold
    def highlight_md(val):
        if val > threshold:
            return f"🚨 higher than 10% missing"
        else:
            return f"{val:.2f}%"
    
    # Apply the highlighting function to each missing percentage value
    missing_summary['MissingPercentage_Display'] = missing_summary['MissingPercentage'].apply(highlight_md)
    
    # Return the summary table with percentages and highlight text
    return missing_summary


#----------------------------------------------------------------------------------------

def detect_flight_duration_outliers(df: pd.DataFrame, threshold: float = 1.5):
    """
    Use the Interquartile Range (IQR) method to detect outliers in 'Flight Duration'.
    Returns both a summary count and the detailed outlier rows.
    """
    col = "Flight Duration"
    
    # Check if the required column exists, else raise an error
    if col not in df.columns:
        raise ValueError(f"'{col}' column not found in DataFrame.")
    
    # Calculate the 25th percentile (Q1) and 75th percentile (Q3)
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    
    # Compute the interquartile range
    IQR = Q3 - Q1
    
    # Calculate the lower and upper bounds for outlier detection
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    
    # Create a boolean mask to identify outliers outside the bounds
    mask = (df[col] < lower_bound) | (df[col] > upper_bound)
    
    # Count how many outliers we found
    outlier_count = mask.sum()
    
    # Calculate the percentage of outliers relative to total rows
    outlier_percentage = (outlier_count / len(df)) * 100
    
    # Prepare a summary DataFrame for easy reporting
    outlier_summary = pd.DataFrame([{
        "Column": col,
        "OutlierCount": outlier_count,
        "OutlierPercentage": outlier_percentage,
        "OutlierPercentage_Display": f"🚨 **{outlier_percentage:.2f}%**" if outlier_count > 0 else f"{outlier_percentage:.2f}%"
    }])
    
    # Extract detailed rows that are outliers and add a reason column
    detailed_outliers = df[mask].copy()
    detailed_outliers["OutlierReason"] = "Unusual flight duration"
    
    return outlier_summary, detailed_outliers


#----------------------------------------------------------------------------------------


def detect_exact_duplicates(df: pd.DataFrame):
    """
    Find exact duplicate rows in the DataFrame, including all instances of duplicates.
    Returns a DataFrame containing only those duplicate rows.
    """
    # duplicated(keep=False) marks all duplicates, not just subsequent ones
    exact_duplicates = df[df.duplicated(keep=False)].copy()
    
    return exact_duplicates


#----------------------------------------------------------------------------------------


def detect_duplicate_flight_numbers(df: pd.DataFrame, flight_col: str = "Flight Number"):
    """
    Identify flight numbers that appear more than once, excluding missing values,
    and return a count of how many times each duplicated flight number occurs.
    """
    # Confirm the flight number column exists
    if flight_col not in df.columns:
        raise ValueError(f"'{flight_col}' not found in DataFrame.")

    # Filter out rows where the flight number is missing
    df_non_null = df[df[flight_col].notna()]
    
    # Count occurrences of each flight number
    counts = df_non_null.groupby(flight_col).size().reset_index(name='Count')
    
    # Select only those flight numbers that occur more than once
    duplicated_flights = counts[counts['Count'] > 1]

    return duplicated_flights


#----------------------------------------------------------------------------------------


def validate_data(df):
    """
    Validate various code columns against expected regex patterns.
    Returns:
      - invalid_counts: number of invalid values per column
      - invalid_rows_dict: dict of DataFrames with invalid rows for each column
    """
    results = {}

    # Check Airport Code format: exactly 3 uppercase letters
    results['Airport Code'] = ~df['Airport Code'].fillna("").str.match(r'^[A-Z]{3}$')

    # Check Airport GPS Code format: exactly 4 uppercase letters
    results['Airport GPS Code'] = ~df['Airport GPS Code'].fillna("").str.match(r'^[A-Z]{4}$')

    # Check Airport Region Code format: two letters, dash, then 2 or 3 letters (e.g. CC-XX or CC-XXX)
    results['Airport Region Code'] = ~df['Airport Region Code'].fillna("").str.match(r'^[A-Z]{2}-[A-Z]{2,3}$')

    # Check Flight Airline Code format: 2 or 3 uppercase letters
    results['Flight Airline Code'] = ~df['Flight Airline Code'].fillna("").str.match(r'^[A-Z]{2,3}$')

    # Flight Number must start with airline code followed by digits
    def flight_number_invalid(row):
        airline_code = row['Flight Airline Code']
        flight_number = row['Flight Number']
        if pd.isna(airline_code) or pd.isna(flight_number):
            return True  # Invalid if either is missing
        pattern = rf'^{airline_code}\d+$'
        return not re.match(pattern, flight_number)

    # Apply the flight number validation row-wise
    results['Flight Number'] = df.apply(flight_number_invalid, axis=1)

    # Count invalid values for each column
    invalid_counts = {col: mask.sum() for col, mask in results.items()}

    # Create dict of DataFrames holding rows with invalid values per column (optional for display)
    invalid_rows_dict = {}
    for col, mask in results.items():
        invalid_rows_dict[col] = df.loc[mask, [col]]

    return invalid_counts, invalid_rows_dict


#----------------------------------------------------------------------------------------


def summary_stats(df):
    """
    Generate some basic summary statistics about the flight data.
    Returns a dictionary with:
      - Number of flights per arrival country
      - Count of unique airlines
      - Minimum flight duration
      - Maximum flight duration
    """
    stats = {}

    stats['Flights per Arrival Country'] = df['Flight Arrival Country'].value_counts()
    stats['Unique Airlines'] = df['Flight Airline Code'].nunique()
    stats['Shortest Flight Duration'] = df['Flight Duration'].min()
    stats['Longest Flight Duration'] = df['Flight Duration'].max()

    return stats


#----------------------------------------------------------------------------------------


def main():
    # Load the dataset from the SQLite DB file and specified table
    df = load_data('airport_data.db', 'MOCK_DATA')
    
    # Analyze missing data and get a summary with highlight display
    missing_summary= analyze_missing_values(df, threshold=10.0)
    
    # Print missing data report to console
    print("📊 Missing Values Summary:")
    print(missing_summary)


    # Detect outliers in flight duration and get detailed outlier info
    outlier_summary, detailed_outliers = detect_flight_duration_outliers(df)

    print("📊 Outlier Summary:")
    print(outlier_summary)

    print("\n🚨 Detailed Outliers:")
    print(detailed_outliers.head())

    # Detect exact duplicate rows anywhere in the DataFrame
    print("\n🚨 duplicated rows:")
    exact_dupes = detect_exact_duplicates(df)
    print(f"Found {len(exact_dupes)} duplicated rows")
    print(exact_dupes)


    # Detect duplicated flight numbers and print a summary table
    print("\n🚨 duplicate flight numbers:")
    duplicated_summary = detect_duplicate_flight_numbers(df)
    print(duplicated_summary.to_markdown(index=False))


if __name__ == "__main__":
    main()
