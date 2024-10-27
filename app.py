import os
import csv
import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup as bs


dir_path = 'data/'

"""
# Where Is My Promise
## Talento Teck Hackathon

Aplicacion para localizar locales comerciales en arriendo 
"""


def cleanCsv():
    inFile = 'data/Real_Estate_Sales_2001_2022_GL.csv'
    df = pd.read_csv(inFile)
    df1 = df.dropna()
    df1.to_csv("data/Real_Estate_Sales_2001_2022_GL_1.csv", index=False)


@st.cache_data
def readCsv():
    datafile = 'data/Real_Estate_Sales_2001_2022_GL_1.csv'

    data = []
    with open(datafile, 'r') as csvdata:
        dataDict = csv.DictReader(csvdata)
        print("reading...")

        for row in dataDict:
            location = row['Location']
            point = location.split("(")[-1].split(")")[0].split( )
            longitude = point[0]
            latitude = point[-1]
            data.append({
                'latitude': float(latitude),
                'longitude': float(longitude)
            })
        
    return data


def mapping():
    data = readCsv()

    st.header('Realstate in USA')
    st.map(data, zoom=7.5)




# cleanCsv()
mapping()
# scrapping()
# readCsv()


