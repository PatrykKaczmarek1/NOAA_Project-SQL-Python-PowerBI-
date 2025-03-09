import requests
import pyodbc

#Access the credentials
credentials = {}
with open("C:/Users/Patryk/Documents/Python Learning/NOAA Project/Credentials.txt", 'r') as file:
    for line in file:
        key, value = line.strip().split('=')
        credentials[key] = value

# Define the parameters
start_date = "2025-01-01"
record_limit = 1000  # Maximum limit allowed by the API
token = credentials.get('token')

# Construct the base URL
base_url = f"https://www.ncei.noaa.gov/cdo-web/api/v2/stations?limit={record_limit}&startdate={start_date}"

# Set the headers
headers = {
    "Content-Type": "application/json",
    "token": token,
    "Accept": "application/json"
}

# Initialize variables
all_results = []
record_offset = 1

# Loop to retrieve all data
while True:
    url = f"{base_url}&offset={record_offset}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        response_results = response_data.get('results')
        if not response_results:
            break
        all_results.extend(response_results)
        record_offset += record_limit
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        break

# Define the Azure authentication parameters
driver = "{ODBC Driver 18 for SQL Server}"
username = credentials.get('username')
password = credentials.get('password')
server = credentials.get('server')
database = credentials.get('database')

conn_str = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={database};
    UID={username};
    PWD={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
"""
try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful!")
    cursor = conn.cursor()

    # Insert retrieved data into Stations stable
    if all_results:
        table_name = 'Stations'
        valid_columns = ["elevation", "mindate", "maxdate", "latitude", "name", "datacoverage", "id", "elevationUnit", "longitude"]
        columns = ', '.join(valid_columns)
        placeholders = ', '.join(['?' for _ in valid_columns])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        for row in all_results:
            values = [row.get(col, None) for col in valid_columns]
            cursor.execute(insert_query, values)
        conn.commit()
    
    # Close the connection
    cursor.close()
    conn.close()
except Exception as e:
    print("Error connecting to database:", e)