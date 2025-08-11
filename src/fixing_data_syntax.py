#run this script only once
import re

# Read the broken SQL file (because theres no "" around the columns names)
with open('MOCK_DATA (1).sql', 'r') as file:
    sql_script = file.read()

# Regex to find the column list part of the insert statement
pattern = r'INSERT INTO (\w+)\s*\((.*?)\)\s*VALUES'
matches = re.finditer(pattern, sql_script, re.IGNORECASE | re.DOTALL)

# Fix each match
for match in matches:
    table_name = match.group(1)
    columns_raw = match.group(2)
    
    # Split by commas, strip spaces, and wrap in double quotes
    columns = [f'"{col.strip()}"' for col in columns_raw.split(',')]
    fixed_columns = ', '.join(columns)
    
    # Original and fixed insert header
    original = match.group(0)
    fixed = f'INSERT INTO {table_name} ({fixed_columns}) VALUES'

    # Replace in the script
    sql_script = sql_script.replace(original, fixed)

# Save the fixed version
with open('MOCK_DATA_fixed.sql', 'w') as file:
    file.write(sql_script)

print("✅ Fixed SQL file saved as 'MOCK_DATA_fixed.sql'")
