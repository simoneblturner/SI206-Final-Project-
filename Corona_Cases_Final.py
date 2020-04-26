import requests
import sqlite3

def country_list_corona():
    #Pulling Corona Cases & Deaths API Information
    url = "https://coronavirus-monitor-v2.p.rapidapi.com/coronavirus/cases_by_country.php"
    headers = {
        'x-rapidapi-host': "coronavirus-monitor-v2.p.rapidapi.com",
        'x-rapidapi-key': "0703ba965emsheeeaf0cc17ceeeep1f13dbjsnf8a169011985"}

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    country_names = []
    for dictionary in data["countries_stat"]:
        country_names.append(dictionary['country_name'])

    return country_names
