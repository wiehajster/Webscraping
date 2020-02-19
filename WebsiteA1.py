from website import Website

class WebsiteA1(Website):
    
    def __init__(self, scraper, infos):
        super().__init__(scraper, infos)
    
    def create_links(self,infos):
        print("A1 - creating links")
        links = []
        for info in infos:
            info = info + "a1"
            links.append(info)
        self.print_list(links)
        return links
    
    def initialize_next_website(self):
        print("A1 - initializing next website")
        return None
