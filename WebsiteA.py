from ScraperA1 import ScraperA1
from website import Website
from WebsiteA1 import WebsiteA1



class WebsiteA(Website):
    
    def __init__(self, scraper, infos):
        Website.__init__(self, scraper, infos)
    
    
    def create_links(self,infos):
        print("A - creating links")
        links = []
        for info in infos:
            info = info + "a"
            links.append(info)
        self.print_list(links)
        return links
    
    def initialize_next_website(self):
        print("A - initializing next website")
        website = WebsiteA1(ScraperA1(), self.get_results())
        return website
    
    