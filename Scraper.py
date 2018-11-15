# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 02:18:44 2018

@author: rdas3
"""
import urllib
import requests
#import bs4
from bs4 import BeautifulSoup
import pandas as pd
#import re
#import csv
import time

YOUR_STATE = 'North Carolina'

url_template = "http://www.indeed.com/jobs?q=continental&l={}&start={}"

# loops through each city in the city list, and loops through each page with search results for that city
# 100 results per page, 10 pages per city --> 1000 job postings per city
# each time this cell is run the results list resets aka is empty (note this does not affect my dataframe)
# each job posting is appended to the results list (as html text)
# use append method, rather than list comprehension so data isn't overwritten
# sleep 1 sec between each url request
max_results_per_city = 200 # Set this to a high-value (5000) to generate more results. 
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
df_more = pd.DataFrame(columns=["Title","Location","Company","Salary", "Synopsis"])
for city in set(['IL', 'TX', 'MI', YOUR_STATE]):
    for start in range(0, max_results_per_city, 10):
        # Grab the results from the request (as above)
        url = url_template.format(city, start) #Try changing this to look up states instead of cities
        # Append to the full set of results
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
        for each in soup.find_all(class_= "result" ):
      #      try:                                                                            #Handling Network Errors
       #         requests.get("http://www.indeed.com/jobs?q=continental&l={}&start={}")
        #    except requests.exceptions.RequestException:
         #       pass  # handle the exception. maybe wait and try again later    
            try: 
                Jobtype = each.find('div', attrs={'data-tn-component': 'organicJob'}).text.replace('\n', '') # To scrape only organic jobs and not sponsored ads
            except:
                title = "Nan"
            try: 
                title = each.find(class_='jobtitle').text.replace('\n', '')
            except:
                title = "Nan"
            try:
                location = each.find('span', {'class':"location" }).text.replace('\n', '')
            except:
                location = "Nan"
            try: 
                company = each.find(class_='company').text.replace('\n', '')
            except:
                company = "Nan"
            try:
                job_posted = each.find(class_='date').text.replace('\n', '')
            except:
                job_posted = "Nan"
            try:
                salary = each.find(class_='no-wrap').text.replace('\n', '')
            except:
                salary = "NaN"
            try:
                synopsis = each.find('span', {'class':'summary'}).text.replace('\n', '')
            except:
                synopsis = "NaN"
            df_more = df_more.append({'days since post':job_posted,'Title':title, 'Location':location, 'Company':company, 'Salary':salary, 'Synopsis':synopsis}, ignore_index=True)
            i += 1
            if i % 1000 == 0:  #  counter to see how many. 
                print('You have ' + str(i) + ' results. ' + str(df_more.drop_duplicates()) + " of these aren't rubbish.")
            df_more.drop_duplicates(keep='first')
            df_more.to_csv(r'C:\Users\rdas3\Desktop\data_Continental_15th_Test_Nov.csv', encoding='utf-8')


                                               #Unreliable HTTP connection Error Handling
                                               #If you’re scraping an unreliable website or you are behind an unreliable internet connection, you may sometimes get HTTPErrors or URLErrors for valid URLs. Trying again later might help.
                                               #This function tries to download the page thee times. On the first two fails, it waits 42 seconds and tries again. On the third failure, it raises the error. On a success, it returs the content of the page.
def load(url):                                 #URL Error Handling
    retries = 3
    for i in range(retries):
        try:
            handle = urllib.urlopen(url)
            return handle.read()
        except urllib.URLError:
            if i + 1 == retries:
                raise
            else:
                time.sleep(42)
    # never get here

print ('Data Written to CSV File')            

    
    
    
    
    
    
    
