import json
import requests
import sqlite3

url = "https://ebola-outbreak.p.rapidapi.com/cases"

headers = {
    'x-rapidapi-host': "ebola-outbreak.p.rapidapi.com",
    'x-rapidapi-key': "0703ba965emsheeeaf0cc17ceeeep1f13dbjsnf8a169011985"
    }

response = requests.request("GET", url, headers=headers)

data = response.json()

#print(response.text)
#print(data)

num = 1
for case in data:
    case["date"] = num
    num += 1

conn = sqlite3.connect('Ebola.db')
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cases(
        date INTEGER PRIMARY KEY,
        cases INTEGER,
        deaths INTEGER
    )
    """
)

for i in data:
    cur.execute(
        """
        INSERT INTO cases(date, cases, deaths)
        VALUES (?, ?, ?)
        """,
        (i['date'], i['cases'], i['deaths']))

conn.commit()
    