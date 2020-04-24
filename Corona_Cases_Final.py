import requests
import sqlite3
import Pollution
import Popul-by-Country

#Pulling Corona Cases & Deaths API Information
url = "https://coronavirus-monitor-v2.p.rapidapi.com/coronavirus/cases_by_country.php"
headers = {
    'x-rapidapi-host': "coronavirus-monitor-v2.p.rapidapi.com",
    'x-rapidapi-key': "0703ba965emsheeeaf0cc17ceeeep1f13dbjsnf8a169011985"}

response = requests.request("GET", url, headers=headers)
data = response.json()

conn = sqlite3.connect('Corona_Cases2.db')
cur = conn.cursor()

#Creating Corona Cases & Deaths Table
#cur.execute("""CREATE TABLE IF NOT EXISTS Cases(Country PRIMARY KEY,Cases INTEGER,Deaths INTEGER)""")

index = 0
for dictionary in data["countries_stat"]:
   if index < 20:
        cur.execute(
           """
           INSERT INTO Cases(Country, Cases, Deaths)
           VALUES (?, ?, ?)
           """, 
           (dictionary['country_name'], dictionary['cases'], dictionary['deaths']))
    index += 1

    conn.commit() 

#Below we start filtering based on the countries that we all have in common

#Pulling Grace's Data
pollution_countries = Pollution.country_list()

#Pulling Simone's Data
#Popul-by-Country.XX

country_names = []
for dictionary in data["countries_stat"]:
    country_names.append(dictionary['country_name'])
country_names = sorted(country_names)

list_of_country_dicts = []
id_number = 0
for country in country_names:
    if country in pollution_countries and in XX:
        for country_dict in data["countries_stat"]:
            if country_dict["country_name"] == country:
                new_corona_dict = {}
                new_corona_dict["id"] = id_number
                new_corona_dict["Country"] = country_dict["country_name"]
                new_corona_dict["Cases"] = dictionary["cases"]
                new_corona_dict["Deaths"] = dictionary["deaths"]
                list_of_country_dicts.append(new_corona_dict)
                id_number += 1
            else:
                continue
    else:
        continue

print(list_of_country_dicts)

#Below we create the filtered table
