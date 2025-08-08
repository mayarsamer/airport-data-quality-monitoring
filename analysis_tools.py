import sqlite3
import pandas as pd

def load_data(db_path: str, table_name: str) -> pd.DataFrame:
    """Connect to the SQLite database and return the table as a DataFrame."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    conn.close()
    return df

def analyze_missing_values(df: pd.DataFrame, threshold: float = 10.0):
    """Calculate % missing per column and add a Markdown-friendly highlight."""
    
    missing_percentages = df.isnull().mean() * 100
    missing_summary = missing_percentages.reset_index()
    missing_summary.columns = ['Column', 'MissingPercentage']
    
    # Add a "Display" column for Markdown with emoji for high-missing
    def highlight_md(val):
        if val > threshold:
            return f"🚨 higher than 10% missing"
        else:
            return f"{val:.2f}%"
    
    missing_summary['MissingPercentage_Display'] = missing_summary['MissingPercentage'].apply(highlight_md)
    
    return missing_summary


def detect_outliers(df: pd.DataFrame, numeric_columns=None, threshold=1.5):
    
    """
    Detect outliers in numeric columns using the IQR method.
    Returns:
        outlier_summary: DataFrame with counts and percentages of outliers per column
        outlier_rows: DataFrame containing only the rows with outliers
    """
    if numeric_columns is None:
        numeric_columns = df.select_dtypes(include='number').columns.tolist()
    
    outlier_flags = pd.DataFrame(False, index=df.index, columns=numeric_columns)
    
    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        outlier_flags[col] = (df[col] < lower_bound) | (df[col] > upper_bound)
    
    # Count & percentage of outliers per column
    outlier_summary = outlier_flags.sum().reset_index()
    outlier_summary.columns = ['Column', 'OutlierCount']
    outlier_summary['OutlierPercentage'] = (outlier_summary['OutlierCount'] / len(df)) * 100
    
    # Add Markdown-friendly highlight
    def highlight_md(val):
        return f"🚨 **{val:.2f}%**" if val > 0 else f"{val:.2f}%"
    
    outlier_summary['OutlierPercentage_Display'] = outlier_summary['OutlierPercentage'].apply(highlight_md)
    
    # Get all rows where any column has an outlier
    outlier_rows = df[outlier_flags.any(axis=1)]
    
    return outlier_summary, outlier_rows


def main():
    # Load data
    df = load_data('airport_data.db', 'MOCK_DATA')
    
    # Analyze missing values
    missing_summary= analyze_missing_values(df, threshold=10.0)
    
    # For now, just print results
    print("📊 Missing Values Summary:")
    print(missing_summary)


if __name__ == "__main__":
    main()
