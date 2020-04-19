from bs4 import BeautifulSoup
import requests
import re
import os

baseurl = "https://www.numbeo.com"
r = requests.get("https://www.numbeo.com/pollution/rankings_by_country.jsp?title=2020&displayColumn=0")
soup = BeautifulSoup(r.text, "html.parser")

Countrynames2020 =[]

Countrynames = soup.find_all("td", class_ = "cityOrCountryInIndicesTable")
for country in Countrynames:
    country = country.text
    Countrynames2020.append(country)
#print(Countrynames2020)

Pollution2020 = []

Pollution = soup.find_all("td", class_ = "sorting_1")
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
    if country1 in Countrynames2020:
        Countrynames2019.append(country1)
#print(Countrynames2019)

Pollution2019 = []
Pollution2 = soup.find_all("td", style = "text-align: right", class_ = "sorting_1")
for num in Pollution2:
    num = num.text
    Pollution2019.append(num)
#print(Pollution2019)









