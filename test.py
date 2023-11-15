import mysql.connector
import os
from datetime import datetime
mydb = mysql.connector.connect(
  host="localhost",
  user=os.environ.get('db_username'),
  password=os.environ.get('db_password'),
  database=os.environ.get('db_name')
)
data_tuple = (2,56.5,999,datetime.now())
cur = mydb.cursor()

write_query = "INSERT INTO reading_reading (temperature_data,pressure_data,moisture_data,created_at) VALUES (%s,%s,%s,%s);"
read_query = "SELECT * FROM reading_reading;"
cur.execute(write_query,data_tuple)
mydb.commit()
cur.execute(read_query)
for row in cur:
    print(row)