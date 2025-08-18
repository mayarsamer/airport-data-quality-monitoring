# ✈️ Airport Data Quality Monitor

## 📌 Project Overview
The **Airport Data Quality Monitor** is a Python-based tool designed to **detect, analyze, and report** data quality issues in airport and flight datasets stored in a SQLite database.

This project:
- Extracts data via **SQL queries**
- Performs **data quality checks**:
  - Missing values detection
  - Outlier detection (e.g., unrealistic flight durations)
  - Duplicate row detection
  - Duplicate flight number detection (excluding null values)
- Generates a **Markdown analysis report**
- extended with a **Streamlit dashboard** for interactive exploration

---

## 🛠 Features
- **SQL Integration** → Connects directly to a local SQLite database.
- **Modular Python functions** for each type of analysis.
- **Data Quality Checks**:
  - **Missing Values** → Calculates percentage of missing data per column and flags high-missing columns.
  - **Outlier Detection** → Detects abnormal flight durations using statistical methods (IQR).
  - **Duplicate Rows** → Finds exact duplicates across all columns.
  - **Duplicate Flight Numbers** → Flags flights with the same number, excluding missing values.
- **Automated Reporting** → Outputs results to `data_quality_report.md` in Markdown format.

---

## 📂 Project Structure

airport-DQ-monitor/

  Data/
  
      │── create_airport_DB.py # Script to create and populate SQLite DB from .sql file ## already done 
      │── MOCK_DATA_fixed.sql #  the data we're using in SQL format
      │── airport_data.db # SQLite database file 
  src/
  
      │── analysis_tools.py # All reusable analysis functions
      │── data_quality_monitor.py # Main execution script that runs all analyses and creates the report
      │── data_quality_report.md # Generated Markdown report
      │── README.md # Project documentation

## 🚀 How to Run

### 1️⃣ Install Requirements
This project uses **uv** for environment and dependency management.  

If you don’t have `uv` installed yet:
```bash
pip install uv
```
Then install all dependencies from pyproject.toml:
```bash
uv sync
```

(This will ensure you have all required packages like pandas, tabulate, and streamlit for the dashboard.)

then activate the virtual enviroment

```bash
source .venv/bin/activate

```

##  2️⃣ change directory to src file

```bash
cd src
```


## 3️⃣ run the streamlit dashboard to see all the analysis done on this data set and interact with it 

```bash
streamlit run streamlit_app.py
```
at the end of the streamlit page you'll find a button that allows you generate an .md report that checks the quality of this data

or you can just simply run data_quality_monitor.py and it will generate the report for you
























