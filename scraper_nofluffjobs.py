from Scraper import Scraper
from bs4 import BeautifulSoup
import re
import ast
import pandas as pd

class Scraper_level_1(Scraper):

    def scrape(self, url):
        response = super().scrape(url)
        soup = response.text
    
        soup = re.sub('true', 'True', soup)
        soup = re.sub('false', 'False', soup)
        d = ast.literal_eval(soup)
        
        df = pd.DataFrame(d['postings'])
        return df

class Scraper_level_2(Scraper):
    
    
    def scrape(self, url):
        response = super().scrape(url)
        soup = response.text
    
        soup = re.sub('true', 'True', soup)
        soup = re.sub('false', 'False', soup)
        soup = re.sub('null', 'None', soup)
        
        
        d = ast.literal_eval(soup)
        
        keys_to_remove = ['companyUrl', 'likes', 'posted', 'status', 'consents', 'meta']
        
        for key in keys_to_remove:
            if key in d:
                del d[key]
                
        df = pd.DataFrame()
        
        df['offerId'] = [d['id']]
        
        df['title'] = [d['title']]
        
        df['website'] = ['nofluffjobs']
        
        base_url = 'https://nofluffjobs.com/job/'
        url = base_url + d['postingUrl']
        df['url'] = [url]
        
        company = d['company']
        df['company'] = company['name']
        
        location = d['location']
        places = location['places']
        '''
        print(str(places) + '\n')
        print(str(places[0]) + '\n')
        print(str(places[1]) + '\n')
        '''
        
        country_name = ''
        city_name = ''
        
        for place in places:
            if 'country' in place:
                country = place['country']
                country_name = country_name + country['name'] + ', '
            if 'city' in place:
                city_name = city_name + place['city'] + ', ' 
        
        df['country'] = re.sub(',\s+$','',country_name)
        
        df['city'] = re.sub(',\s+$','',city_name)
        
        essentials = d['essentials']
        salary = essentials['salary']['types']
        
        s = ''
        for k, v in salary.items():
            s = s + k + ': ' + str(v['range']) + ', '
        
        df['salary'] = s[:-2]
        
        seo = d['seo']
        df['description'] = [seo['description']]
        
        tags = self.concat_all_strings(d, '|', False)
        
        items_to_remove = ['None', 'main', 'False']
        tags = self.remove_from_tags(tags, items_to_remove)
        df['tags'] = tags
        
        return df
    
    

'''
scraper = Scraper_level_1()
df = scraper.scrape('https://nofluffjobs.com/api/search/posting?region=pl')
base_url = 'https://nofluffjobs.com/api/posting/'
ending = '?city=remote&region=pl'
urls = []
for index, row in df.iterrows():
    url = base_url + str(row['id']) + ending
    urls.append(url)
    break



scraper = Scraper_level_2()
d = scraper.scrape('https://nofluffjobs.com/api/posting/RACTYDZA?city=remote&region=pl')

with pd.ExcelWriter('results.xlsx', engine="openpyxl", mode='a') as writer:  

    d.to_excel(writer, sheet_name='Sheet1', index = False)
#d.to_excel('results.xlsx', index = False, mode = 'a')
'''