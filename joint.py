import requests
from bs4 import BeautifulSoup
import re
import json
import os
import sqlite3
import Pollution
import Population
import Corona_Cases_Final
import matplotlib
import matplotlib.pyplot as plt

# CREATE DATABASE
conn = sqlite3.connect('COVID_Pollution_Correlation.db')
cur = conn.cursor()

# CREATE UNIVERSAL KEY FOR EVERY COUNTRY
def create_database():
    
    pollution = Pollution.country_list_pollution()
    population = Population.country_list_population()
    corona = Corona_Cases_Final.country_list_corona()

    merged_list = population + pollution + corona
    all_countries = list(set(merged_list))
    all_countries = sorted(all_countries)

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Country_ids(
            country_id INTEGER PRIMARY KEY,
            country_name STRING NOT NULL
        )
        """
    )
    i = 0 
    for country in all_countries: 
        i += 1
        cur.execute(
            """
            INSERT INTO Country_ids(country_id, country_name)
            VALUES (?, ?)
            """,
            (i, country)
        )

    conn.commit()

# CREATE POPULATION TABLE

def population_data():
    url = "https://ajayakv-rest-countries-v1.p.rapidapi.com/rest/v1/all"

    headers = {
        'x-rapidapi-host': "ajayakv-rest-countries-v1.p.rapidapi.com",
        'x-rapidapi-key': "02e0a7d154mshbc0feed6cd14574p180afajsn055d7cf35fd7"
        }

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS popul_density(
            country_id INTEGER PRIMARY KEY,
            country_name STRING,
            population INTEGER,
            area FLOAT, 
            density FLOAT

        )
        """
    )
    
    index = 0
    
    for country in data:
        country_name = country["name"]
        cur.execute("SELECT country_id FROM Country_ids WHERE country_name = ?", (country_name,))
        name = cur.fetchone()[0]
        try:
            if index < 150: 
                density = country["population"] / country["area"]
                cur.execute(
                    """
                    INSERT INTO popul_density(country_id, country_name, population, area, density)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (name, country_name, country['population'], country["area"], density))
                index += 1 
        except:
            continue 

    conn.commit()

#CREATE POLLUTION TABLE 

def pollution_data():
    r = requests.get("https://www.numbeo.com/pollution/rankings_by_country.jsp?title=2020&displayColumn=0")
    soup = BeautifulSoup(r.text, "html.parser")

    Countrynames2020 =[]

    Countrynames = soup.find_all("td", class_ = "cityOrCountryInIndicesTable")
    for country in Countrynames:
        country = country.text
        Countrynames2020.append(country)

    Pollution2020 = []

    Pollution = soup.find_all("td", style = "text-align: right")
    for number in Pollution:
        number = number.text
        Pollution2020.append(number)

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

    cur.execute("CREATE TABLE IF NOT EXISTS pollution2019 (id INTEGER PRIMARY KEY, country STRING, pollution_index FLOAT)")
    for i in tup2019:
        cur.execute("SELECT country_id FROM Country_ids WHERE country_name = ?", (i[0],))
        name = cur.fetchone()[0]
        cur.execute("INSERT INTO pollution2019 (id,country, pollution_index) VALUES (?, ?, ?)",(name, i[0], i[1]))
    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS pollution2020 (id INTEGER PRIMARY KEY, country STRING, pollution_index FLOAT)")
    for i in tup2020:
        cur.execute("SELECT country_id FROM Country_ids WHERE country_name = ?", (i[0],))
        name = cur.fetchone()[0]
        cur.execute("INSERT INTO pollution2020 (id, country, pollution_index) VALUES (?,?,?)",(name, i[0],i[1]))
    conn.commit()

# CREATE COVID CASES TABLE

def covid_case_data():
    url = "https://coronavirus-monitor-v2.p.rapidapi.com/coronavirus/cases_by_country.php"
    headers = {
        'x-rapidapi-host': "coronavirus-monitor-v2.p.rapidapi.com",
        'x-rapidapi-key': "0703ba965emsheeeaf0cc17ceeeep1f13dbjsnf8a169011985"}

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    cur.execute("""CREATE TABLE IF NOT EXISTS Cases(country_id PRIMARY KEY, country_name STRING, cases INTEGER, deaths INTEGER)""")

    for country in data["countries_stat"]:
        country_name = country["country_name"]
        cur.execute("SELECT country_id FROM Country_ids WHERE country_name = ?", (country_name,))
        name = cur.fetchone()[0]
        cur.execute(
        """
        INSERT INTO Cases(country_id, country_name, cases, deaths)
        VALUES (?, ?, ?, ?)
        """, 
        (name, country['country_name'], country['cases'], country['deaths']))
    
    conn.commit() 

# JOIN CASES DATA AND POPULATION DENSITY DATA

def cases_density():

    print("\n Density vs Cases \n")

    cur.execute(
    '''
    SELECT Country_ids.country_name, popul_density.density, Cases.cases 
    FROM Cases 
    INNER JOIN popul_density 
    ON Cases.country_id = popul_density.country_id 
    INNER JOIN Country_ids
    ON Cases.country_id = Country_ids.country_id

    '''
    )
    conn.commit()
    all = cur.fetchall()

    tups = []
    for i in all: 
        tups.append(i)

    # Plot Density vs Cases
    names = []
    density = []
    cases = []
    print(tups)
    for tup in tups:
        names.append(tup[0])
        density.append(tup[1])
        stri = str(tup[2])
        if "," in stri:
            num = float(stri.replace(",", ""))
            cases.append(num)
        else:
            cases.append(float(stri))
   
    plt.figure(1, figsize = (9,3))
    plt.scatter(density, cases)
    #plt.set_xlabel("Population Density")
    #plt.set_ylabel("COVID-19 Cases")
    #plt.set_title("Population Density by County vs COVID-19 Cases")
    plt.savefig("DENSITY_CASES.png")
    plt.show()

# JOIN CASES DATA AND POLLUTION 2019 DATA

def cases_2019():

    print("\nCases vs Pollution 2019 \n")

    cur.execute(
    '''
    SELECT Country_ids.country_name, Cases.cases, pollution2019.pollution_index 
    FROM Cases 
    INNER JOIN pollution2019 
    ON Cases.country_id = pollution2019.id
    INNER JOIN Country_ids
    ON Cases.country_id = Country_ids.country_id

    '''
    )
    conn.commit()
    tups = []
    all = cur.fetchall()
    for i in all: 
        tups.append(i)    



# JOIN CASES DATA AND POLLUTION 2020 DATA

def cases_2020():

    print("\nCases vs Pollution 2020 \n")

    cur.execute(
    '''
    SELECT Country_ids.country_name, Cases.cases, pollution2020.pollution_index 
    FROM Cases 
    INNER JOIN pollution2020 
    ON Cases.country_id = pollution2020.id
    INNER JOIN Country_ids
    ON Cases.country_id = Country_ids.country_id

    '''
    )
    conn.commit()
    all = cur.fetchall()
    for i in all: 
        print(i)


# RUN FUNCTIONS
create_database()
population_data()
pollution_data()
covid_case_data()

cases_density()
cases_2019()
cases_2020()

