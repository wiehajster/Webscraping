from Scraper import Scraper
from bs4 import BeautifulSoup
import re
import ast
import pandas as pd

class Scraper_level_1(Scraper):
    
    def __init__(self):
        super().__init__()
    
    def scrape(self, url):
        response = super().scrape(url)
        soup = response.text
    
        soup = re.sub('true', 'True', soup)
        soup = re.sub('false', 'False', soup)
        d = ast.literal_eval(soup)
        
        df = pd.DataFrame(d['postings'])
        return df

class Scraper_level_2(Scraper):
    
    def __init__(self):
        super().__init__()
    
    
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
        country = places[1]['country']
        df['country'] = country['name']
        city = places[1]['city']
        df['city'] = city
        
        essentials = d['essentials']
        salary = essentials['salary']
        salary = salary['types']
        s = ''
        for i in salary:
            s = s + i + '|'
            s = s + self.concat_all_strings(salary[i], '|', True) + '|'
        df['salary'] = s[:-1]
        
        seo = d['seo']
        df['description'] = [seo['description']]
        
        tags = self.concat_all_strings(d, '|', False)
        
        items_to_remove = ['None', 'main', 'False']
        tags = self.remove_from_tags(tags, items_to_remove)
        df['tags'] = tags
        print(tags)
        
        return df
    
    


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