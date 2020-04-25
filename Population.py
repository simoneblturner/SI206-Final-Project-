from bs4 import BeautifulSoup
import requests
import re
import os
import sqlite3

#PART 1 -- Get List of Countries from Funcation and Data

def country_list_population():

    list_population = []

    url = "https://ajayakv-rest-countries-v1.p.rapidapi.com/rest/v1/all"

    headers = {
        'x-rapidapi-host': "ajayakv-rest-countries-v1.p.rapidapi.com",
        'x-rapidapi-key': "02e0a7d154mshbc0feed6cd14574p180afajsn055d7cf35fd7"
        }

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    for country in data:
        list_population.append(country["name"])
    
    return list_population
