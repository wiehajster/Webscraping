from Scraper import Scraper


class ScraperA(Scraper):
    
    def __init__(self):
         super().__init__()
    
    def scrape(self,link):
        print("A \n")
        return "A"
    