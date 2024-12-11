import psycopg2
import datetime
import requests
import time
from tqdm.auto import tqdm

connection = "postgresql://overcat:overmind@localhost:5432/stockdata"

conn = psycopg2.connect(connection)
cursor = conn.cursor()

year0 = datetime.date.today().year
year1 = 2021
stock = 'LOFC'

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

start_time = 0
end_time = 0
for year in tqdm(range(year0, year1, -1)):

    start = str(int(datetime.datetime(year, 12, 31, 5, 30).timestamp()))
    end = str(int(datetime.datetime(year -1 , 12, 31, 5, 30).timestamp()))
    url = f"https://charts.atradsolutions.com/atsweb/twchart?action=history&format=json&symbol={stock}.N0000&from={end}&to={start}&firstDataRequest=true&resolution=1D"
    time_diff = end_time - start_time

    print(f"request for year: {year} | {time_diff}")
    res = requests.get(url)

    dict = res.json()

    start_time = time.time()
    for i in tqdm(range(len(dict["t"]))):
        
        cursor.execute(f"""
            INSERT INTO {stock} (timestamp, open_price, close_price, high_price, low_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING
        """, (
            dict["t"][i], 
            dict["o"][i], 
            dict["c"][i], 
            dict["h"][i], 
            dict["l"][i], 
            dict["v"][i]
        ))
    end_time = time.time()

conn.commit()

cursor.close()
conn.close()



