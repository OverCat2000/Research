import psycopg2
import datetime
import requests
import time
from tqdm.auto import tqdm
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Download stock data and store it in a PostgreSQL database.")
parser.add_argument("--year1", type=int, default=2015, help="Start year for data retrieval (default: 2015).")
parser.add_argument("--stock", type=str, required=True, help="Stock symbol (e.g., LOFC).")

args = parser.parse_args()

# Retrieve arguments
year0 = datetime.date.today().year
year1 = args.year1
stock = args.stock

# Database connection
connection = "postgresql://overcat:overmind@localhost:5432/stocks"
conn = psycopg2.connect(connection)
cursor = conn.cursor()

# Create table if not exists
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {stock} (
        timestamp BIGINT PRIMARY KEY,
        open_price FLOAT,
        close_price FLOAT,
        high_price FLOAT,
        low_price FLOAT,
        volume FLOAT
    )
""")

conn.commit()

# Data retrieval loop
start_time = 0
end_time = 0
for year in tqdm(range(year0, year1, -1)):
    start = str(int(datetime.datetime(year, 12, 31, 5, 30).timestamp()))
    end = str(int(datetime.datetime(year - 1, 12, 31, 5, 30).timestamp()))
    url = f"https://charts.atradsolutions.com/atsweb/twchart?action=history&format=json&symbol={stock}.N0000&from={end}&to={start}&firstDataRequest=true&resolution=1D"
    time_diff = end_time - start_time

    print(f"Request for year: {year} | Time diff: {time_diff}")
    res = requests.get(url)

    if res.status_code != 200:
        print(f"Failed to retrieve data for year {year}. HTTP Status: {res.status_code}")
        continue

    data = res.json()

    if data.get('s') == 'no_data' and data.get('nextTime') == 'NA':
        print(f"No data available for year {year}. API returned 'no_data'. Skipping...")
        continue

    start_time = time.time()
    for i in tqdm(range(len(data["t"]))):
        cursor.execute(f"""
            INSERT INTO {stock} (timestamp, open_price, close_price, high_price, low_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING
        """, (
            data["t"][i], 
            data["o"][i], 
            data["c"][i], 
            data["h"][i], 
            data["l"][i], 
            data["v"][i]
        ))
    end_time = time.time()

conn.commit()

# Close connections
cursor.close()
conn.close()

print("Data retrieval and storage complete.")
