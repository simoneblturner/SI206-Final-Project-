import requests
import json
import sqlite3

url = "https://covid-19-statistics.p.rapidapi.com/reports/total"

dates = ["2020-01-22", "2020-01-23", "2020-01-24", "2020-01-25", "2020-01-26", "2020-01-27", "2020-01-28", "2020-01-29", "2020-01-30", "2020-01-31", "2020-02-01","2020-02-02", "2020-02-03", "2020-02-04", "2020-02-05", "2020-02-06", "2020-02-07", "2020-02-08", "2020-02-09", "2020-02-10", "2020-02-11", "2020-02-12", "2020-02-13", "2020-02-14", "2020-02-15", "2020-02-16", "2020-02-17", "2020-02-18", "2020-02-19", "2020-02-20", "2020-02-21", "2020-02-22", "2020-02-23", "2020-02-24", "2020-02-25", "2020-02-26", "2020-02-27", "2020-02-28", "2020-03-01", "2020-03-02", "2020-03-03", "2020-03-04", "2020-03-05", "2020-03-06", "2020-03-07", "2020-03-08", "2020-03-09", "2020-03-10", "2020-03-11", "2020-03-12", "2020-03-13", "2020-03-14", "2020-03-15", "2020-03-16", "2020-03-17", "2020-03-18", "2020-03-19", "2020-03-20", "2020-03-21", "2020-03-22", "2020-03-23", "2020-03-24", "2020-03-25", "2020-03-26", "2020-03-27", "2020-03-28", "2020-03-29", "2020-03-30", "2020-03-31", "2020-04-01", "2020-04-02", "2020-04-03", "2020-04-04", "2020-04-05", "2020-04-06", "2020-04-07"]
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


conn = sqlite3.connect('COVID-19.db')
cur = conn.cursor()

num = 1 
for date in covid_information:
    date["data"]["date"] = num
    num += 1

print(covid_information)

#Confirmed Cases Table 

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS confirmed(
        date INTEGER PRIMARY KEY,
        confirmed INTEGER

    )
    """
)

for day in covid_information:
    dct = day["data"]
    cur.execute(
        """
        INSERT INTO confirmed(date, confirmed)
        VALUES (?, ?)
        """,
        (dct['date'], dct['confirmed']))

conn.commit()

#Death table 

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS deaths(
        date INTEGER PRIMARY KEY,
        deaths INTEGER

    )
    """
)
for day in covid_information:
    dct = day["data"]
    cur.execute(
        """
        INSERT INTO deaths(date, deaths)
        VALUES (?, ?)
        """,
        (dct['date'], dct['deaths']))

conn.commit()