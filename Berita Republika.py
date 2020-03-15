#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import requests
import datetime
from bs4 import BeautifulSoup


# In[2]:


page = requests.get("https://www.republika.co.id")
obj = BeautifulSoup(page.text, 'html.parser')
current = datetime.datetime.now()


# In[3]:


list = []
count = 0

for terkini in obj.find_all('div', class_='teaser_conten1'):
    latest = {
        "category": str(terkini.find('p').text),
        "title": str(terkini.find('h2').text),
        "upload": str(terkini.find('div', class_='date').text),
        "update": str(current.strftime('%IY-%m-%d %H:%M:%S %p'))
    }
    list.append(latest)

with open("dump.json", "w") as json_file:
    json.dump(list, json_file)


# In[ ]:




