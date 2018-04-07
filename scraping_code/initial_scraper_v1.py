
# coding: utf-8

# In[17]:


import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# In[5]:


root = "/home/chris/"


# In[6]:


## transform raw songs list into searchable terms

data_raw = pd.read_csv(root + "wordplay/data/songs_csv.csv")


# In[9]:


data_raw.head()


# In[10]:


data_raw["search_term"] = data_raw["Song"].map(str) + ' by ' + data_raw["Artist"].map(str)


# In[12]:


data_raw.head(20)


# In[15]:


data_raw["search_term"][6
                ]


# In[19]:


## driver
driver = webdriver.Firefox()


# In[ ]:




