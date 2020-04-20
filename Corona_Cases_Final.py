import requests
import sqlite3

url = "https://coronavirus-monitor-v2.p.rapidapi.com/coronavirus/cases_by_country.php"

headers = {
    'x-rapidapi-host': "coronavirus-monitor-v2.p.rapidapi.com",
    'x-rapidapi-key': "0703ba965emsheeeaf0cc17ceeeep1f13dbjsnf8a169011985"
    }

response = requests.request("GET", url, headers=headers)

#print(response.text)
data = response.json()

country_names = []
for dictionary in data["countries_stat"]:
    country_names.append(dictionary['country_name'])
print(country_names)

conn = sqlite3.connect('Corona_Cases2.db')
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS Cases(
        Country PRIMARY KEY,
        Cases INTEGER,
        Deaths INTEGER
    )
    """
    )

for dictionary in data["countries_stat"][:20]:
    cur.execute(
        """
        INSERT INTO Cases(Country, Cases, Deaths)
        VALUES (?, ?, ?)
        """,
        (dictionary['country_name'], dictionary['cases'], dictionary['deaths']))

conn.commit() 