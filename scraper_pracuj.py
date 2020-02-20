from Scraper import Scraper
from bs4 import BeautifulSoup
import re
import ast
import pandas as pd
import numpy as np
from collections import defaultdict

class Scraper_level_1(Scraper):
    
    
    def scrape(self, url):
        response = super().scrape(url)
        soup = BeautifulSoup(response.text, 'lxml')
    
        last_page_nr = soup.find_all('li', class_='pagination_element-page')[-1]
        last_page_nr = int(last_page_nr.text)
        return 2
        

class Scraper_level_2(Scraper):
        
    def scrape(self, url):
        response = super().scrape(url)
        soup = response.text
        start = re.search(r'window.__INITIAL_STATE__ = ', soup)
        end = re.search(';\s*var __RAWURL__ = ', soup)
        
    
        json = soup[start.end(): end.start()]
        json = re.sub('true', 'True', json)
        json = re.sub('false', 'False', json)
    
        d = ast.literal_eval(json)
        
        
        keys_to_drop = ['companyId', 'companyProfileUrl', 'employmentForm', 'expirationDate', 'lastPublicated', 'logo',
                           'mainCategoriesIds', 'offerType', 'optionalCv', 'salaryId', 'employmentLevel', 'remoteWork',
                           'typesOfContract', 'workSchedules']
        
        offers = d['offers']
        
        for key in keys_to_drop:
            for offer in offers:
                if key in offer:
                    del offer[key]
        
        df = pd.DataFrame(offers)
        
        columns = {
                'commonOfferId' : 'offerId',
                'jobTitle' : 'title',
                'employer' : 'company',
                'countryName' : 'country',
                'jobDescription' : 'description'
                }
        
        
        df = df.rename(columns = columns)
        
        cities = [offer['offers'][0]['label'] for offer in offers]
        df['city'] = cities
        del df['offers']
        df['website'] = 'pracuj'
        df['url'] = url
           
        return (d, offers,  df)
        

url = 'https://www.pracuj.pl/praca'
scraper = Scraper_level_1()    
last_page_nr = scraper.scrape(url)
    
new_urls = []
base_url = 'https://www.pracuj.pl/praca/ds;kw?pn='
    
for i in range(1, last_page_nr + 1):
    new_urls.append(base_url + str(i))

scraper = Scraper_level_2()
results = []
for url in new_urls:
    results.append(scraper.scrape(url))
    break
final_df = results 
#final_df = pd.concat(results)
#final_df.to_excel('results.xlsx', index=False)

'''
with pd.ExcelWriter('results.xlsx', engine="openpyxl", mode='a') as writer:  

    final_df.to_excel(writer, sheet_name='Sheet1', index = False)         
'''