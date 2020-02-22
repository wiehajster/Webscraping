from website import Website
from scraper_pracuj import Scraper_level_2
import pandas as pd

class Website_level_1(Website):
    
    def create_links(self,infos):
        url = 'https://www.pracuj.pl/praca/it;kw'
        urls = []
        urls.append(url)
        return urls
    
    def initialize_next_website(self):
        return Website_level_2(Scraper_level_2(), self.get_results())

class Website_level_2(Website):
       
    def create_links(self,infos):
        urls = []
        base_url = 'https://www.pracuj.pl/praca/it;kw?pn='
    
        for last_page_nr in infos:
            for i in range(1, last_page_nr + 1):
                urls.append(base_url + str(i))
            
        return urls
    
    def initialize_next_website(self):
        final_df = pd.concat(self.get_results())
        final_df.to_excel('results.xlsx', index=False)
        return None
