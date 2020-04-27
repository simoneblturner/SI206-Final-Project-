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

# PART ONE CREATE ONE DATABASE FOR ALL INFORMATION
conn = sqlite3.connect('COVID_Pollution_Correlation.db')
cur = conn.cursor()

# PART TWO CREATE UNIVERSAL KEY FOR EVERY COUNTRY
def create_database():
    
    # TAKE LIST OF COUNTRIED FROM THREE SEPARATH FILES
    # FILES: Population.py outputs country_list_population 
    # FILES: Pollution.py outputs country_list_pollution
    # FILES: Corona_Cases_Final.py outputs country_list_corona
    pollution = Pollution.country_list_pollution()
    population = Population.country_list_population()
    corona = Corona_Cases_Final.country_list_corona()

    # MERGE LISTS FROM 2 APIS AND WEBSITE
    # ONE LARGE, UNIVERSAL, SORTED LIST OF COUNTRIES WITHOUT DUPLICATES
    merged_list = population + pollution + corona
    all_countries = list(set(merged_list))
    all_countries = sorted(all_countries)

    # CREATE TABLE TO ASSIGN UNIVERSAL ID TO EACH COUNTRY TO USE AS PRIMARY KEY
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Country_ids(
            country_id INTEGER PRIMARY KEY UNIQUE,
            country_name STRING NOT NULL UNIQUE
        )
        """
    )

    # CHECK NUMBER OF ROWS IN Country_ids TABLE
    cur.execute(
        """ 
        SELECT COUNT (*) FROM Country_ids
        """
        )
    c = cur.fetchone()[0]
    i = c

    # INSERT 20 ROWS AT A TIME
    # RUN FUNCTION MULITPLE TIMES TO GET MORE ROWS
    for country in all_countries[c:c+20]: 
        i += 1
        try:
            cur.execute(
            
            """
            INSERT INTO Country_ids(country_id, country_name)  
            VALUES (?, ?)
            """,
            (i, country)
            )
            
        except:
            continue
        
    conn.commit()

# PART THREE FUNCTION TO CREATE TABLE FOR POLLUTION DATA

def population_data():
    # REQUEST AND GET DATA FROM API
    url = "https://ajayakv-rest-countries-v1.p.rapidapi.com/rest/v1/all"

    headers = {
        'x-rapidapi-host': "ajayakv-rest-countries-v1.p.rapidapi.com",
        'x-rapidapi-key': "02e0a7d154mshbc0feed6cd14574p180afajsn055d7cf35fd7"
        }

    response = requests.request("GET", url, headers=headers)

    # TURN DATA INTO JSON FILE
    data = response.json()

    # CREATE POPULATION DENSITY TABLE IN COVID_Pollution_Correlation.db 
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

    # CHECK THE NUMBER OF ROWS IN popul_density

    cur.execute(
        """ 
        SELECT COUNT (*) FROM popul_density
        """
    )

    c = cur.fetchone()[0]

    # INSERT 20 ROWS AT A TIME INTO popul_density TABLE FROM data
    # ASSIGN PRIMARY ID KEY TO ALL THE COUNTRIES 
    for country in data[c:c+20]:
        country_name = country["name"]
        cur.execute("SELECT country_id FROM Country_ids WHERE country_name = ?", (country_name,))
        name = cur.fetchone()[0]
        try:
            density = country["population"] / country["area"]
            cur.execute(
                """
                INSERT INTO popul_density(country_id, country_name, population, area, density)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, country_name, country['population'], country["area"], density))
             
        except:
            continue 

    conn.commit()

# PART FOUR FUNCTION TO CREATE POLLUTION TABLE 

def pollution_data():
    # REQUEST DATA FROM WEBSITE 
    r = requests.get("https://www.numbeo.com/pollution/rankings_by_country.jsp?title=2020&displayColumn=0")
    soup = BeautifulSoup(r.text, "html.parser")

    # PUT POLLUTION COUNTRIES INTO LIST - 2020
    Countrynames2020 =[]

    Countrynames = soup.find_all("td", class_ = "cityOrCountryInIndicesTable")
    for country in Countrynames:
        country = country.text
        Countrynames2020.append(country)

    # PUT POLLUTION DATA INTO LISTS - 2020
    Pollution2020 = []

    Pollution = soup.find_all("td", style = "text-align: right")
    for number in Pollution:
        number = number.text
        Pollution2020.append(number)

    r = requests.get("https://www.numbeo.com/pollution/rankings_by_country.jsp?title=2019&displayColumn=0")
    soup = BeautifulSoup(r.text, "html.parser")

    # PUT POLLUTION COUNTRIES INTO LIST - 2019
    Countrynames2019 = []
    Countrynames2 = soup.find_all("td", class_ = "cityOrCountryInIndicesTable")
    for country1 in Countrynames2:
        country1 = country1.text
        Countrynames2019.append(country1)

    # PUT POLLUTION DATA INTO LIST - 2019 
    Pollution2019 = []
    Pollution2 = soup.find_all("td", style = "text-align: right")
    for num in Pollution2:
        num = num.text
        Pollution2019.append(num) 

    # PUT 2019 POLLUTION DATA INTO TUPLES
    tup2019 = []
    for x in range(len(Countrynames2019)):
        tup = (Countrynames2019[x],Pollution2019[x])
        tup2019.append(tup)

    # PUT 2020 POLLUTION DATA INTO TUPLES
    tup2020 =[]
    for x in range(len(Countrynames2020)):
        if Countrynames2020[x] in Countrynames2019:
            tup = (Countrynames2020[x],Pollution2020[x])
            tup2020.append(tup)

    # SORT TUPLES
    tup2019 = sorted(tup2019)
    tup2020 = sorted(tup2020)

    # CREATE 2019 POLLUTION TABLE
    cur.execute("CREATE TABLE IF NOT EXISTS pollution2019 (id INTEGER PRIMARY KEY, country STRING, pollution_index FLOAT)")
    
    # CHECK NUMBER OF ROWS IN POLLUTION 2019 TABLE
    cur.execute(
        """ 
        SELECT COUNT (*) FROM pollution2019
        """
    )
    c = cur.fetchone()[0]

    # INSERT 20 ITEMS INTO TABLE AT A TIME 
    # RUN AS MANY TIMES TO GATHER AND INSERT ALL OF THE INFORMATION 
    for i in tup2019[c:c+20]:
        # MATCH UNIVERSAL COUNTRY ID TO COUNTRY IN POLLUTION DATA 
        cur.execute("SELECT country_id FROM Country_ids WHERE country_name = ?", (i[0],))
        name = cur.fetchone()[0]
        cur.execute("INSERT INTO pollution2019 (id,country, pollution_index) VALUES (?, ?, ?)",(name, i[0], i[1]))
    conn.commit()

    # CREATE TABLE FOR POLLUTION 2020 
    cur.execute("CREATE TABLE IF NOT EXISTS pollution2020 (id INTEGER PRIMARY KEY, country STRING, pollution_index FLOAT)")
    
    # CHECK HOW MANY ROWS ARE IN pollution2020 
    cur.execute(
        """ 
        SELECT COUNT (*) FROM pollution2020
        """
    )

    con = cur.fetchone()[0]
    
    # INSERT 20 ITEMS INTO TABLE AT A TIME 
    # RUN AS MANY TIMES TO GATHER AND INSERT ALL OF THE INFORMATION
    for i in tup2020[con:con+20]:
        # MATCH UNIVERSAL COUNTRY ID TO COUNTRY IN POLLUTION DATA 
        cur.execute("SELECT country_id FROM Country_ids WHERE country_name = ?", (i[0],))
        name = cur.fetchone()[0]
        cur.execute("INSERT INTO pollution2020 (id, country, pollution_index) VALUES (?,?,?)",(name, i[0],i[1]))
    conn.commit()

# PART FIVE FUNCRION TO CREATE COVID CASES TABLE

def covid_case_data():
    # GET DATA FROM CORONA API
    url = "https://coronavirus-monitor-v2.p.rapidapi.com/coronavirus/cases_by_country.php"
    headers = {
        'x-rapidapi-host': "coronavirus-monitor-v2.p.rapidapi.com",
        'x-rapidapi-key': "0703ba965emsheeeaf0cc17ceeeep1f13dbjsnf8a169011985"}

    response = requests.request("GET", url, headers=headers)
    
    # PUT DATA INTO JSON FORMAT 
    data = response.json()

    # CREATE Cases TABLE 
    cur.execute("""CREATE TABLE IF NOT EXISTS Cases(country_id PRIMARY KEY, country_name STRING, cases INTEGER, deaths INTEGER)""")
    
    # CHECK HOW MANY ROWS ARE IN Cases
    cur.execute(
        """ 
        SELECT COUNT (*) FROM Cases
        """
    )

    c = cur.fetchone()[0]

    # INSERT 20 ROWS INTO Cases FROM COVID-19 DATA
    # RUN THIS FUNCTION AS MANY TIMES TO GET AND INSERT ALL OF THE DATA
    for country in data["countries_stat"][c:c+20]:
        country_name = country["country_name"]
        # MATCH IDS FOR COUNTRIES BETWEEN EACH TABLE
        cur.execute("SELECT country_id FROM Country_ids WHERE country_name = ?", (country_name,))
        name = cur.fetchone()[0]
        cur.execute(
        """
        INSERT INTO Cases(country_id, country_name, cases, deaths)
        VALUES (?, ?, ?, ?)
        """, 
        (name, country['country_name'], country['cases'], country['deaths']))
    
    conn.commit() 

# CHECK HOW MANY ROWS ARE IN Country_ids
cur.execute(
        """ 
        SELECT COUNT (*) FROM Country_ids
        """
    )
one = cur.fetchone()[0]

# RUN THE FIRST FUNCTION UNTIL ALL THE DATA IS IN THE DATABASE/TABLE
if one == 281:
    # START RUNNING SECOND FUNCTION
    population_data()
    # CHECK HOW MANY ROWS ARE IN popul_density FROM THE SECOND FUNCTION 
    cur.execute(
            """ 
            SELECT COUNT (*) FROM popul_density
            """
        )
    two = cur.fetchone()[0]
    # RUN UNTIL popul_density TABLE HAS ALL 240 DATA ROWS 
    if two == 240:
        #START RUNNING THIRD FUNCTION 
        pollution_data()
        # CHECK HOW MANY ROWS ARE IN pollution 2019 FROM THE THIRD FUNCTION 
        cur.execute(
            """ 
            SELECT COUNT (*) FROM pollution2019
            """
            )
        three = cur.fetchone()[0]
        # RUN UNTIL pollution2019 AND pollution2020 TABLES HAVE ALL THE DATA INSERTED 
        if three == 106:
            # START RUNNING FOURTH FUNCTION 
            covid_case_data()
            # FOURTH FUNCTION MAKES THE Cases TABLE - CHECK HOW MANY ROWS ARE IN THE TABLE 
            cur.execute(
                """ 
                SELECT COUNT (*) FROM Cases
                """
                )
            four = cur.fetchone()[0]

# THERE IS SO MUCH DATA FROM OUR THREE SOURCES GOING INTO ONE DATABASE
# WE CAN ONLY DO IT 20 ITEMS AT A TIME 
# IN ORDER TO INSERT ALL THE DATA YOU MUST RUN THE FILE MANY TIMES 
# ONCE THE DATABASE IS CREATED AND FULL, CAN USE TO RUN VISUALIZATIONS 