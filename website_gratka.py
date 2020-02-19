from gratka import Gratka_Actual_Scraper
from website import Website
import pandas as pd

class Gratka_Initial_Website(Website):
    
    def create_links(self,infos):
        city_name = 'kielce'
        url = f'https://gratka.pl/nieruchomosci/mieszkania/{city_name}/wynajem'
        urls = []
        urls.append(url)
        return urls
    
   
    def initialize_next_website(self):
        return Gratka_Actual_Website(Gratka_Actual_Scraper(), self.get_results())
    
class Gratka_Actual_Website(Website):
    
    def create_links(self,infos):
        city_name = 'kielce'
        base_url = f'https://gratka.pl/nieruchomosci/mieszkania/{city_name}/wynajem'
        
        urls = []
        for last_page in infos:
            for i in range(1, last_page+1):
                url = base_url + f'?page={i}'
                urls.append(url)
            return urls
    
   
    def initialize_next_website(self):
        
        df = pd.concat(self.results)
        df.to_excel('gratka.xlsx', index=False)
        return None