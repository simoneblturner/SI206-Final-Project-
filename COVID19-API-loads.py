import requests
import json
import sqlite3

url = "https://covid-19-statistics.p.rapidapi.com/reports/total"

dates = ["2020-02-07", "2020-02-08", "2020-02-09", "2020-02-10"]
covid_information = []

for date in dates:

    querystring = {"date": date}

    headers = {
        'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
        'x-rapidapi-key': "02e0a7d154mshbc0feed6cd14574p180afajsn055d7cf35fd7"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    covid_information.append(data)
    
#print(covid_information)

conn = sqlite3.connect('COVID-19.db')
cur = conn.cursor()

num = 1 
for date in covid_information:
    date["data"]["date"] = num
    num += 1

print(covid_information)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS cases(
        date INTEGER PRIMARY KEY,
        confirmed INTEGER,
        deaths INTEGER

    )
    """
)

for day in covid_information:
    dct = day["data"]
    cur.execute(
        """
        INSERT INTO cases(date, confirmed, deaths)
        VALUES (?, ?, ?)
        """,
        (dct['date'], dct['confirmed'], dct['deaths']))

conn.commit()