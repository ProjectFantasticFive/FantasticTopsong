#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import time
import re
import json
from datetime import datetime


# In[2]:


web = requests.get("https://republika.co.id/")
soup = BeautifulSoup(web.content, 'html.parser')


# In[3]:


headlines = soup.find_all('p', {"class": "link-headline"})

print("Main Headlines :")
for head in headlines:
    print(head.text)


# In[4]:


def getPublicationTime(url):
    req = requests.get(url)
    sup = BeautifulSoup(req.content, 'html.parser')
    
    raw_time = sup.find('div', {"class": "date_detail"})
    raw_time = raw_time.text.replace('WIB', '')
    raw_time = re.sub(' +', ' ', raw_time)
    raw_time = raw_time.strip()
#     time = datetime.strptime(raw_time.strip(), "%A %d %b %Y %H:%M")
    return raw_time


# In[5]:


def write_json(data, filename='dump.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 


# In[7]:


lastest = soup.find_all('div', {"class": "teaser_conten1_center"})
lastest_array = []

print("Lastest news :")
for last in lastest:
    if last.find('div', {"class": "clear"}) != None:
        continue
    
    print("Kategori\t: " + last.find('h1').find('a').text)
    print("Judul\t\t: " + last.find('h2').text)
    print("Waktu Scrapping\t: " + time.strftime("%b %d %Y %H:%M:%S"))
    
    time_pub = getPublicationTime(last.find('h2').find('a').get('href'))
    print("Waktu Publikasi\t: " + time_pub)
    
    x = {
        "categories": str(last.find('h1').find('a').text),
        "title": str(last.find('h2').text),
        "scrapped_time": str(time.strftime("%b %d %Y %H:%M:%S")),
        "published_time": str(time_pub)
    }
    
    lastest_array.append(x)


# In[8]:


lastest_array[0]


# In[9]:
    

with open('dump.json') as json_file: 
    try:
        data = json.load(json_file)
        data.update(lastest_array)
    
        write_json(data)
    except:
        write_json(lastest_array)



