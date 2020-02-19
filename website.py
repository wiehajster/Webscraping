from abc import ABC,abstractmethod 

class Website(ABC):
    
    def __init__(self, scraper, infos):
        self.links = self.create_links(infos)
        self.scraper = scraper
        self.results = []
     
    def create_links(self,infos):
        pass
    
    def start_scraping(self):
        result = self.scraper.scrape(self.links.pop(0))
        self.results.append(result)
        
    def is_empty(self):
        if not self.links:
            return True
        return False
    
    @abstractmethod
    def initialize_next_website(self):
        pass
    
    def get_results(self):
        return self.results
    
    def print_list(self,list):
        for element in list:
            print(element + "\n")
        
        
    
    
    