from bs4 import BeautifulSoup
import requests
import re
import os
import sqlite3

def country_list_pollution():
    r = requests.get("https://www.numbeo.com/pollution/rankings_by_country.jsp?title=2020&displayColumn=0")
    soup = BeautifulSoup(r.text, "html.parser")

    Countrynames2020 =[]

    Countrynames = soup.find_all("td", class_ = "cityOrCountryInIndicesTable")
    for country in Countrynames:
        country = country.text
        Countrynames2020.append(country)
    #print(Countrynames2020)

    Pollution2020 = []

    Pollution = soup.find_all("td", style = "text-align: right")
    for number in Pollution:
        number = number.text
        Pollution2020.append(number)
    #print(Pollution2020)

    r = requests.get("https://www.numbeo.com/pollution/rankings_by_country.jsp?title=2019&displayColumn=0")
    soup = BeautifulSoup(r.text, "html.parser")

    Countrynames2019 = []
    Countrynames2 = soup.find_all("td", class_ = "cityOrCountryInIndicesTable")
    for country1 in Countrynames2:
        country1 = country1.text
        Countrynames2019.append(country1)

    Pollution2019 = []
    Pollution2 = soup.find_all("td", style = "text-align: right")
    for num in Pollution2:
        num = num.text
        Pollution2019.append(num)

    tup2019 = []
    for x in range(len(Countrynames2019)):
        tup = (Countrynames2019[x],Pollution2019[x])
        tup2019.append(tup)

    tup2020 =[]
    for x in range(len(Countrynames2020)):
        if Countrynames2020[x] in Countrynames2019:
            tup = (Countrynames2020[x],Pollution2020[x])
            tup2020.append(tup)

    tup2019 = sorted(tup2019)
    tup2020 = sorted(tup2020)

    return Countrynames2019
