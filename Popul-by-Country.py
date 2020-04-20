import requests
import json
import sqlite3

url = "https://ajayakv-rest-countries-v1.p.rapidapi.com/rest/v1/all"

headers = {
    'x-rapidapi-host': "ajayakv-rest-countries-v1.p.rapidapi.com",
    'x-rapidapi-key': "02e0a7d154mshbc0feed6cd14574p180afajsn055d7cf35fd7"
    }

response = requests.request("GET", url, headers=headers)

data = response.json()

print(data)

conn = sqlite3.connect('Popul-density.db')
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS popul_density(
        country PRIMARY KEY,
        population INTEGER,
        area FLOAT, 
        density FLOAT

    )
    """
)

index = 20

for country in data[:index]:
    try:

        density = country["population"] / country["area"]
        cur.execute(
            """
            INSERT INTO popul_density(country, population, area, density)
            VALUES (?, ?, ?, ?)
            """,
            (country['name'], country['population'], country["area"], density))
           
    except:
        continue 

conn.commit()
