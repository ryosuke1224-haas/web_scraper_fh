#!/usr/bin/env python
# coding: utf-8

import requests
import time
import pandas as pd
import csv
from selenium import webdriver
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
import bs4

links=pd.read_csv('links_findahaunt.csv',header=None)
links

for i in links[0]:
    print(i)

names=[]
adresses=[]
webs=[]
phones=[]
for i in links[0]:
    try:
        res = requests.get(i)
        individualpage = BeautifulSoup(res.text, 'lxml')
        name = individualpage.find("article",class_="content-listing").find("h1").text
        names.append(name)
        try:
            adress=individualpage.find("article",class_="content-listing").find('p').find("a").text
            adresses.append(adress)
        except:
            adresses.append('cannot find')
        try:
            web=individualpage.find("a",class_="hauntsite").get("href")
            web=web.replace('?utm_source=FindAHaunt.com&utm_medium=website&utm_campaign=HauntedHouseMedia','')
            webs.append(web)
        except:
            webs.append('cannot find')   
        
        try:
            phone=individualpage.find_all(text=re.compile(r'\d\d\d-\d\d\d-\d\d\d\d'))
            phones.append(phone)
        except:
            phones.append('cannot find')
    except:
        pass

df=pd.DataFrame({"name":names,
    "adress":adresses,
    "website":webs,
    "phone":phones   
})

df_new=df.drop_duplicates(["name"])

df_new.to_csv('output_findahaunt.csv')
