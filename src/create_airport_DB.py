import sqlite3
#creating a database locally
# Connect to DB
conn = sqlite3.connect('airport_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS MOCK_DATA (
        "Airport Code" TEXT,
        "Airport GPS Code" TEXT,
        "Airport Region Code" TEXT,
        "Flight Arrival Country" TEXT,
        "Flight Arrival City" TEXT,
        "Flight Duration" INTEGER,
        "Flight Number" TEXT,
        "Flight Departure Airport" TEXT,
        "Flight Airline Code" TEXT
    );
''')

with open('MOCK_DATA_fixed.sql', 'r') as file:
    sql_script = file.read()
    cursor.executescript(sql_script)

conn.commit()
conn.close()
