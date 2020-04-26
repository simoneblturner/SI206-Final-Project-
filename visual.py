import requests
from bs4 import BeautifulSoup
import re
import json
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

conn = sqlite3.connect("COVID_Pollution_Correlation.db")
cur = conn.cursor()

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
    fig, ax = plt.subplots()
    ax.scatter(density, cases)
    ax.set_xlabel("Population Density")
    ax.set_ylabel("COVID-19 Cases")
    ax.set_title("Population Density by County vs COVID-19 Cases")
    plt.savefig("DENSITY_CASES.png")
    plt.show()

# JOIN CASES DATA AND POLLUTION 2019 DATA
def difference_in_pollution():

    print("\n Difference in Pollution 2019/2020\n")
    
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
    all = cur.fetchall()
    tups = []
    for i in all: 
        tups.append(i)
   
    with open("pollution_difference.txt", "w") as output:
        output.write("Country Name, Pollution 2019, Pollution 2020, Pollution Difference\n")
        for tup in tups:
            stri = ""
            for word in tup:
                word = str(word)
                stri += word + " "

            output.write(str(stri) + "\n")


def cases_difference():

    print("\nCases vs Pollution 2019 \n")

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
    tups = []
    all = cur.fetchall()
    for i in all: 
        tups.append(i)    
    
    difference = []
    cases = []
    cases_nums = []
    
    for tup in tups:
        difference.append(tup[4])
        cases.append(tup[1])
    for case in cases:
        case = str(case)
        if "," in case:
            num = float(case.replace(",", ""))
        cases_nums.append(num)

    plt.figure(1, figsize = (9, 3))
    fig, ax = plt.subplots()
    ax.scatter(cases_nums, difference)
    ax.set_xlabel("COVID-19 Cases")
    ax.set_ylabel("Change in Pollution")
    ax.set_title("COVID-19 Cases vs Change in Pollution")
    plt.savefig("DIFFERENCE_CASES.png")
    plt.show()


def difference_density():
    
    cur.execute(
    '''
    SELECT Country_ids.country_name, popul_density.density, pollution2019.pollution_index, pollution2020.pollution_index,
    round((pollution2019.pollution_index - pollution2020.pollution_index), 2)
    FROM popul_density 
    INNER JOIN pollution2019 
    ON popul_density.country_id = popul_density.country_id 
    INNER JOIN pollution2020
    ON popul_density.country_id = pollution2020.id
    INNER JOIN Country_ids
    ON popul_density.country_id = Country_ids.country_id

    '''
    )
    conn.commit()
    all = cur.fetchall()

    tups = []
    for i in all: 
        tups.append(i)
    
    difference = []
    density = []

    for tup in tups:
        difference.append(tup[1])
        density.append(tup[4])

    plt.figure(1, figsize = (9,3))
    fig, ax = plt.subplots()
    ax.scatter(density, difference)
    ax.set_xlabel("Population Density")
    ax.set_ylabel("Change In Pollution")
    ax.set_title("Population Density by Change in Pollution")
    plt.savefig("DENSITY_DIFFERENCE.png")
    plt.show()

difference_in_pollution()
cases_density()
cases_difference()
difference_density()
