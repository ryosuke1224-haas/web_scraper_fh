#!/usr/bin/env python
# coding: utf-8




get_ipython().system('pip install webdriver-manager')


import requests
import time
import pandas as pd
import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
import bs4


#import postal code
postalcode=pd.read_excel('Zipcodes_for_test.xlsx')

#fill O for zipcode
zip_5=[]
for i in postalcode['Zip']:
    zip_5.append('{0:05d}'.format(i))

browser = webdriver.Chrome(ChromeDriverManager().install())
links=[]
baseurl='https://www.findahaunt.com/'
for i in zip_5:
    url = 'https://www.findahaunt.com/'
    browser.get(url)
    time.sleep(2)
    try:
        search = browser.find_element_by_id("searchbox")
        search.clear()
        search.send_keys(i)
        element=browser.find_element_by_id("submit")
        element.click()
        time.sleep(2)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        operators_name = soup.find_all("a",class_="prohaunt list_name")
        for i in operators_name:
            #print(urljoin(baseurl,i.get("href")))
            links.append(urljoin(baseurl,i.get("href")))
    except:
        pass


links_file=pd.DataFrame(links)


links_file.to_csv('links.csv')


links_file=pd.read_csv('links.csv')


links_file=links_file.drop('Unnamed: 0', axis=1)

links_file=links_file.drop_duplicates()

names=[]
adresses=[]
webs=[]
phones=[]
try:
    for i in links_file["0"]:
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


df=pd.DataFrame({
    "name":names,
    "adress":adresses,
    "website":webs,
    "phone":phones   
})


df.to_csv('output_findahaunt.csv')
