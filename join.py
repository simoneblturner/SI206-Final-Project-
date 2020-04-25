import requests
import re
import os
import sqlite3
import Pollution
import Population
import Corona_Cases_Final

def create_database():
    population = Population.country_list_population()
    pollution = Pollution.country_list_pollution()
    corona = Corona_Cases_Final.country_list_corona()

    merged_list = population + pollution + corona
    all_countries = list(set(merged_list))
    all_countries = sorted(all_countries)

    print(all_countries)
    print(len(all_countries))

    conn = sqlite3.connect('COVID_Pollution_Correlation.db')
    cur = conn.cursor()

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
    
create_database()
