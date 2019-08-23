'''''
--> Package Information:
    --------------------
    This package enables webscraping data from trackanalytics.com for 
    retrieval of PewDiPie's and T-Series's subscriber count data since
    2014 till date

--> Version Control:
    ----------------
    Source:
    -------
        version 1.0, Date: April 23, 2019  
'''''

# ------------< Importing packages >------------

import requests
from bs4 import BeautifulSoup
import pandas as pd

# ------------< Retrieving data >------------
def webScrapeData():
    dates=[]
    subs=[]
    url1="https://www.trackalytics.com/youtube/user/pewdiepie/"
    url2="https://www.trackalytics.com/youtube/user/tseries/"
    html1=requests.get(url1)
    html2=requests.get(url2)
    soup1=BeautifulSoup(html1.text, features="html.parser")
    soup2=BeautifulSoup(html2.text, features="html.parser")

    for i in range(0,len(soup1.tbody.contents)):
        if(i%2 !=0):
           dates.append(soup1.tbody.contents[i].contents[3].get_text())
           subs.append(soup1.tbody.contents[i].contents[5].get_text().split(' ')[0])

    df=pd.DataFrame(data={"Dates":dates, "SubscriberCount":subs})
    df.to_csv("./data/web_scrape/pewdipie.csv", sep=',', index=False)

    dates.clear()
    subs.clear()
    df.drop(['Dates','SubscriberCount'], axis=1)

    for i in range(0,len(soup2.tbody.contents)):
        if(i%2 !=0):
           dates.append(soup2.tbody.contents[i].contents[3].get_text())
           subs.append(soup2.tbody.contents[i].contents[5].get_text().split(' ')[0])

    df=pd.DataFrame(data={"Dates":dates, "SubscriberCount":subs})
    df.to_csv("./data/web_scrape/tseries.csv", sep=',', index=False)

webScrapeData()
