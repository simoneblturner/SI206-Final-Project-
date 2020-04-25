from bs4 import BeautifulSoup
import requests
import re
import os
import sqlite3
#import join

#PART 1 -- Get List of Countries from Funcation 

def country_list_population():

    country_list_population = []

    url = "https://ajayakv-rest-countries-v1.p.rapidapi.com/rest/v1/all"

    headers = {
        'x-rapidapi-host': "ajayakv-rest-countries-v1.p.rapidapi.com",
        'x-rapidapi-key': "02e0a7d154mshbc0feed6cd14574p180afajsn055d7cf35fd7"
        }

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    for country in data:
        country_list_population.append(country["name"])
    
    return country_list_population


#PART 2 
#Adding to database created in join.py

# requesting information on country by population from API
url = "https://ajayakv-rest-countries-v1.p.rapidapi.com/rest/v1/all"

headers = {
    'x-rapidapi-host': "ajayakv-rest-countries-v1.p.rapidapi.com",
    'x-rapidapi-key': "02e0a7d154mshbc0feed6cd14574p180afajsn055d7cf35fd7"
    }

response = requests.request("GET", url, headers=headers)

#turning population data into JSON format 
data = response.json()

#taking database from joint file
join.create_database()

def popultion_data():

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS popul_density(
            id INTEGER PRIMARY KEY,
            country STRING,
            population INTEGER,
            area FLOAT, 
            density FLOAT

        )
        """
    )
    #fetching only 20 coumtries data at a time 
    index = 0

    #creating list of countries 
    country_id = 0 
    #inserting data into table
    for country in data:
        try:
            if index < 100: 
                density = country["population"] / country["area"]
                cur.execute(
                    """
                    INSERT INTO popul_density(id, country, population, area, density)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (country_id, country['name'], country['population'], country["area"], density))
                index += 1 
                country_id += 1 
        except:
            continue 

    #commit table 
    conn.commit()

