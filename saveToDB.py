import pandas as pd
import psycopg2

data = pd.read_csv('data/v1.csv')
columns_names = list(pd.read_csv('data/v1.csv', nrows=1).columns)

conn_string = "host='localhost' dbname='pdt_projekt' user='postgres' password='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
columnsLength = len(data)
sql_string = "INSERT INTO stations (amenity, opening_hours, cards, geo, charging) VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s)"
for i in range(columnsLength):
    #print(data["Access Days Time"][i], data["Cards Accepted"][i], data["Longitude"][i], data["Latitude"][i], data["EV Network"][i])
    cursor.execute(sql_string, ("charging_station", data["Access Days Time"][i], data["Cards Accepted"][i], data["Longitude"][i], data["Latitude"][i], data["EV Network"][i]))

conn.commit()
cursor.close()
