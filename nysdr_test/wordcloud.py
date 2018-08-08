# import os

# from os import path
# import wordcloud as wc # import WordCloud

# In[1]:


import numpy as np
import pandas as pd
import re


# In[2]:


df=pd.read_csv("NYC_obgyn_final.csv", header=None)
df.columns=["Malpractice","Boro","Education","Name","Specialty"]


# In[3]:


def split_out_year(ed):
    try:
        s=re.search(',\n',ed).span()
    except:
        s=(None,None)
    school=ed[0:s[0]]
    year= ed[s[1]:]
    return year
def split_out_school(ed):
    try:
        s=re.search(',\n',ed).span()
    except:
        s=(None,None)
    return ed[0:s[0]]
df['School']=list(map(split_out_school,df.Education))
df['Year']=list(map(split_out_year,df.Education))
df=df.drop("Education",axis=1)
# df=df.drop_duplicates("Name")
# df


# In[4]:


us_states=pd.read_csv("States.csv")
us_states=us_states[us_states.x!='US']
us_states=us_states['x']


# In[5]:


df['State'] = df['School'].str.extract('( [A-Z]{2}$)')
df.State=df.State.str.strip()


# In[6]:


# Finding country where they went to school
ind=-1
countries=[]
for st in df.State:
    ind+=1
    if st in us_states.values:
        countries.append('USA')
    else:
        try:
            country=re.search(', [A-Z]+$',df.School[ind]).group() #{1}[a-z]
            #print(country[2:])
            countries.append(country[2:])#df['School'].str.extract(', [A-Z]{1}[a-z]+$')
        except Exception as e:
            #print(e)
            countries.append('')
            continue
df['Country']=countries


# In[7]:


## TO DO ### Fix New York - NY
#df[df['Country']==''].School


# In[7]:


def find_num_pay(mal):
    # check Judgments and Arbitration Awards
    start,end =re.search('Number of awards:',mal).span()
    try:
        a= int(mal[end+1:end+2])
    except:
        # check Settlements
        start,end_p =re.search('Number of payments:',mal).span()
        a= int(mal[end_p+1:end_p+2])
    return a


# In[8]:


ind=0
num_payments=[]
for m in range(len(df)):
    #print(ind)
    if df.Malpractice[ind]=='None reported':
        num_payments.append(0)
    else:
        a=find_num_pay(df.Malpractice[ind])
        num_payments.append(a)
    ind+=1
df['Num_Payments']=num_payments

# import numpy as np # linear algebra
# import pandas as pd 
import matplotlib as mpl
import matplotlib.pyplot as plt
# %matplotlib inline

from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS

stopwords = set(STOPWORDS)

wordcloud = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40, 
                          random_state=42
                         ).generate(df['School'])

print(wordcloud)
fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()


