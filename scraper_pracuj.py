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
        soup = BeautifulSoup(response.text, 'lxml')
    
        last_page_nr = soup.find_all('li', class_='pagination_element-page')[-1]
        last_page_nr = int(last_page_nr.text)
        return 2
        

class Scraper_level_2(Scraper):
    
    def __init__(self):
        super().__init__()
        
    def scrape(self, url):
        response = super().scrape(url)
        soup = response.text
        start = re.search(r'window.__INITIAL_STATE__ = ', soup)
        end = re.search(';\s*var __RAWURL__ = ', soup)
        
    
        json = soup[start.end(): end.start()]
        json = re.sub('true', 'True', json)
        json = re.sub('false', 'False', json)
    
        d = ast.literal_eval(json)
        
        df = pd.DataFrame(d['offers'])
        columns_to_drop = ['companyId', 'companyProfileUrl', 'employmentForm', 'expirationDate', 'lastPublicated', 'logo',
                           'mainCategoriesIds', 'offerType', 'optionalCv', 'salaryId']
        for column in columns_to_drop:
            del df[column]
        
        columns = {
                'offerId' : 'commonOfferId',
                'title' : 'jobTitle',
                'company' : 'employer',
                'country' : 'countryName',
                'salary' : 'salary',
                'description' : 'jobDescription'
                }
        final_df = pd.DataFrame()
        i = 0
        for x, y in columns.items():
            final_df.insert(i,x, df[y])
            i += 1
        
        final_df['website'] = 'pracuj'
        final_df['url'] = url
        final_df['city'] = ''
        final_df['tags'] = ''
        offers = df['offers']
        
        for index, row in df.iterrows():
            offer = offers.loc[index]
            place_dict = offer[0]
            city = self.concat_all_strings(place_dict['cities'], '|', False)
            final_df.loc[index, 'city'] = city
            tags = self.concat_all_strings(row, '|', False)
            tags = self.remove_from_tags(tags, [','])
            final_df.loc[index, 'tags'] = tags
            
        return final_df
        

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
#final_df = results 
final_df = pd.concat(results)
final_df.to_excel('results.xlsx', index=False)
'''
with pd.ExcelWriter('results.xlsx', engine="openpyxl", mode='a') as writer:  

    final_df.to_excel(writer, sheet_name='Sheet1', index = False)         
''' 
    