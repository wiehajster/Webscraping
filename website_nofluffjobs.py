from website import Website
from scraper_nofluffjobs import Scraper_level_2
import pandas as pd

class Website_level_1(Website):
    
    def __init__(self, scraper, infos):
        super().__init__(scraper, infos)
    
    
    def create_links(self,infos):
        url = 'https://nofluffjobs.com/api/search/posting?region=pl'
        urls = []
        urls.append(url)
        return urls
    
   
    def initialize_next_website(self):
        return Website_level_2(Scraper_level_2(), self.get_results())
    
class Website_level_2(Website):
    
    def __init__(self, scraper, infos):
        super().__init__(scraper, infos)
    
    
    def create_links(self,infos):
        df = infos[0]
        base_url = 'https://nofluffjobs.com/api/posting/'
        ending = '?city=remote&region=pl'
        urls = []
        i = 0
        for index, row in df.iterrows():
            url = base_url + str(row['id']) + ending
            urls.append(url)
            i += 1
            if i == 4:
                break
        return urls
    
   
    def initialize_next_website(self):
        df = pd.concat(self.results)
        df.to_excel('res.xlsx', index=False)
        return None