import streamlit as st
import pandas as pd
import sqlite3
import subprocess
from analysis_tools import load_data, analyze_missing_values, detect_exact_duplicates, detect_duplicate_flight_numbers,detect_flight_duration_outliers, summary_stats,validate_data


DB_PATH = "../data/airport_data.db"
TABLE_NAME = "MOCK_DATA"

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Airport Data Quality Dashboard", layout="wide")
st.title("🛫 Airport Data Quality Monitor")

# --- Load Data ---

df = load_data(DB_PATH, TABLE_NAME)
st.write(f"**Total Rows:** {len(df)}")
st.dataframe(df.head())
filtered_df = df.copy()
tabs = st.tabs(["Missing Values", "Outliers", "Duplicates", "Invalid Codes", "Summary Stats"])

with tabs[0]:
    st.header("📊 Missing Values")
    missing_summary = analyze_missing_values(filtered_df)
    st.dataframe(missing_summary)
    
    st.bar_chart(missing_summary.set_index('Column')['MissingPercentage'])

with tabs[1]:
    st.header("🚨 Flight Duration Outliers")
    outlier_summary, detailed_outliers = detect_flight_duration_outliers(filtered_df)
    st.dataframe(outlier_summary)
    with st.expander("View Detailed Outliers"):
        st.dataframe(detailed_outliers)

with tabs[2]:
    st.header("🔁 Duplicates")
    exact_dupes = detect_exact_duplicates(filtered_df)
    flight_dupes = detect_duplicate_flight_numbers(filtered_df)
    st.write(f"Exact Duplicate Rows: {len(exact_dupes)}")
    st.write(f"Duplicate Flight Numbers: {len(flight_dupes)}")
    with st.expander("View Exact Duplicate Rows"):
        st.dataframe(exact_dupes)
    with st.expander("View Duplicate Flight Numbers"):
        st.dataframe(flight_dupes)

with tabs[3]:
    st.header("🚫 Invalid Codes")
    invalid_counts, invalid_rows = validate_data(filtered_df)
    st.table(pd.DataFrame.from_dict(invalid_counts, orient='index', columns=['Invalid Count']))
    with st.expander("View Invalid Values Detail"):
        for col, invalid_df in invalid_rows.items():
            st.write(f"Invalid values in **{col}** ({len(invalid_df)})")
            if len(invalid_df) > 0:
                st.dataframe(invalid_df)
            else:
                st.write("No invalid values found.")

with tabs[4]:
    st.header("📈 Summary Statistics")
    stats = summary_stats(filtered_df)
    
    st.write("Flights per Arrival Country:")
    st.bar_chart(stats['Flights per Arrival Country'])

    st.write(f"Unique Airlines: {stats['Unique Airlines']}")
    st.write(f"Shortest Flight Duration: {stats['Shortest Flight Duration']}")
    st.write(f"Longest Flight Duration: {stats['Longest Flight Duration']}")

    flights_per_city = filtered_df['Flight Arrival City'].dropna().value_counts()
    st.write("Flights per Arrival City:")
    st.bar_chart(flights_per_city)


# --- side bar, filtering options ---
city_filter = st.sidebar.multiselect("Filter by Arrival City", options=df['Flight Arrival City'].dropna().unique())
country_filter = st.sidebar.multiselect("Select Arrival Country", options=df['Flight Arrival Country'].unique())
airline_filter = st.sidebar.multiselect("Select Airline", options=df['Flight Airline Code'].unique())
airport_filter = st.sidebar.multiselect("Select Airport Code", options=df['Airport Code'].unique())


# Apply each filter if any selection was made
if city_filter:
    filtered_df = filtered_df[filtered_df['Flight Arrival City'].isin(city_filter)]
if country_filter:
    filtered_df = filtered_df[filtered_df['Flight Arrival Country'].isin(country_filter)]
if airline_filter:
    filtered_df = filtered_df[filtered_df['Flight Airline Code'].isin(airline_filter)]
if airport_filter:
    filtered_df = filtered_df[filtered_df['Airport Code'].isin(airport_filter)]


flights_per_city = filtered_df['Flight Arrival City'].dropna().value_counts()

st.subheader(f"📊 (Filtered by selected criteria)")

st.bar_chart(flights_per_city)






# --- Generate Markdown Report ---
st.subheader("📄 Generate Markdown Report")
if st.button("Run Full Analysis & Create Report"):
    result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    st.success("Report generated successfully! Check data_quality_report.md")
    st.code(result.stdout)
