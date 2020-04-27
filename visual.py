import requests
from bs4 import BeautifulSoup
import re
import json
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

# CONNECT TO THE COVID_Pollution_Correlation.db
conn = sqlite3.connect("COVID_Pollution_Correlation.db")
cur = conn.cursor()

# FUNCTION TO JOIN CASES DATA AND POPULATION DENSITY DATA
def cases_density():

    # JOIN TABLES 
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

    # CREATE LIST OF TUPLES 
    tups = []
    for i in all: 
        tups.append(i)

    # Plot Density vs Cases
    names = []
    density = []
    cases = []
    
    # TURN INTO FLOATS
    for tup in tups:
        names.append(tup[0])
        density.append(tup[1])
        stri = str(tup[2])
        if "," in stri:
            num = float(stri.replace(",", ""))
            cases.append(num)
        else:
            cases.append(float(stri))
   
    # CREATE VISUALIXATION
    fig, ax = plt.subplots() 
    ax.scatter(x = density, y = cases, color="red") 
    ax.set_xlabel("Population Density by Country")
    ax.set_ylabel("COVID-19 Cases")
    ax.set_title("Population Density by Country vs COVID-19 Cases")
    plt.savefig("DENSITY_CASES.png")
    plt.show()

# FUNCRION TO JOIN CASES DATA AND POLLUTION 2019 DATA
def difference_in_pollution():
    
    # JOIN TABLES 
    cur.execute(
    '''
    SELECT Country_ids.country_name, pollution2019.pollution_index, 
    pollution2020.pollution_index, round((pollution2019.pollution_index - pollution2020.pollution_index), 2)
    FROM pollution2019
    INNER JOIN pollution2020
    ON pollution2019.id = pollution2020.id
    INNER JOIN Country_ids
    ON pollution2019.id = Country_ids.country_id
    '''
    )
    conn.commit()

    # CREATE LIST OF TUPLES
    all = cur.fetchall()
    tups = []
    for i in all: 
        tups.append(i)
   
    # CREATE TEXT FILE WITH CALCULATION 
    with open("pollution_difference.txt", "w") as output:
        output.write("Country Name, Pollution 2019, Pollution 2020, Pollution Difference\n")
        for tup in tups:
            stri = ""
            for word in tup:
                word = str(word)
                stri += word + ", "

            output.write(str(stri[:-2]) + "\n")

# FUNCTION TO JOIN AND CREATE VISULIZATION FOR CASES AND DIFFERENCE IN POLLUTION BETWEEN 2019-2020
def cases_difference():

    cur.execute(
    '''
    SELECT Country_ids.country_name, Cases.cases, pollution2019.pollution_index, pollution2020.pollution_index,
    round((pollution2019.pollution_index - pollution2020.pollution_index), 2)
    FROM Cases 
    INNER JOIN pollution2019 
    ON Cases.country_id = pollution2019.id
    INNER JOIN pollution2020
    ON Cases.country_id = pollution2020.id
    INNER JOIN Country_ids
    ON Cases.country_id = Country_ids.country_id

    '''
    )
    conn.commit()

    # PUT DATA INTO LIST OF TUPLES
    tups = []
    all = cur.fetchall()
    for i in all: 
        tups.append(i)    
    
    difference = []
    cases = []
    cases_nums = []
    
    # CONVERT STRINGS TO FLOATS 
    for tup in tups:
        difference.append(tup[4])
        cases.append(tup[1])
    for case in cases:
        case = str(case)
        if "," in case:
            num = float(case.replace(",", ""))
        cases_nums.append(num)

    # CREATE VISUALIZATION 
    #plt.figure(2, figsize = (8, 8))
    fig, ax = plt.subplots()
    ax.scatter(cases_nums, difference, color="green")
    ax.set_xlabel("COVID-19 Cases")
    ax.set_ylabel("Change in Pollution")
    ax.set_title("COVID-19 Cases vs Change in Pollution")
    plt.savefig("DIFFERENCE_CASES.png")
    plt.show()

# FUNCTION TO JOIN AND CREATE VISUAL FOR POLLUTION DIFFERENCE AND POPULATION DENSITY 
def difference_density():
    
    # JOIN TABLES 
    cur.execute(
    '''
    SELECT Country_ids.country_name, popul_density.density, pollution2019.pollution_index, pollution2020.pollution_index,
    round((pollution2019.pollution_index - pollution2020.pollution_index), 2)
    FROM popul_density 
    INNER JOIN pollution2019 
    ON popul_density.country_id = pollution2019.id 
    INNER JOIN pollution2020
    ON popul_density.country_id = pollution2020.id
    INNER JOIN Country_ids
    ON popul_density.country_id = Country_ids.country_id

    '''
    )
    conn.commit()
    all = cur.fetchall()

    # CREATE LIST OF TUPLES 
    tups = []
    for i in all: 
        tups.append(i)
    
    difference = []
    density = []
    
    for tup in tups:
        difference.append(tup[4])
        density.append(tup[1])

    # CREATE VISUALIZATION 
    #plt.figure(3, figsize = (8,8))
    fig, ax = plt.subplots()
    ax.scatter(density, difference, color="orange")
    ax.set_xlabel("Population Density")
    ax.set_ylabel("Change In Pollution")
    ax.set_title("Population Density by Change in Pollution")
    plt.savefig("DENSITY_DIFFERENCE.png")
    plt.show()

def rate_cases_deaths():
    cur.execute(
    '''
    SELECT Country_ids.country_id, Country_ids.country_name, Cases.cases, Cases.deaths
    FROM Cases
    INNER JOIN Country_ids
    ON Country_ids.country_id = Cases.country_id
    '''
    )
    conn.commit()
    all = cur.fetchall()

    tups = []
    for i in all: 
        tups.append(i)
    
    cases = []
    deaths = []
    countries = []

    num_cases = []
    num_deaths = []

    for tup in tups:
        countries.append(tup[1])
        cases.append(tup[2])
        deaths.append(tup[3])
    
    for case in cases:
        case = str(case)
        if "," in case:
            case = float(case.replace(",", ""))
        num_cases.append(case)
    
    for death in deaths:
        death = str(death)
        if "," in death:
            death = float(death.replace(",", ""))
        num_deaths.append(death)

    tuples = []
    for x in range(213):
        tuples.append((num_deaths[x], num_cases[1]))

    rates = []
    for tup in tuples:
        rate = round((int(tup[0])/int(tup[1])), 4)
        rates.append(rate)

    num_rates = []
    for rate in rates:
        num_rates.append(round(rate, 4))

    data = []
    for x in range(213):
        data.append((countries[x], num_cases[x], num_deaths[x], num_rates[x]))

    with open("rates_cases_deaths.txt", "w") as output:
        output.write("Country Name, Cases, Deaths, Rate of Deaths Per Case\n")
        for x in data: 
            output.write(str(x) + "\n")  

difference_in_pollution()
cases_density()
cases_difference()
difference_density()
rate_cases_deaths()