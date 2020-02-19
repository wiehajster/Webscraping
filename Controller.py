import time

class Controller:
    
    STOP_TIME = 1
    
    def __init__(self, websites):
        self.websites = websites
        
    def scraping(self):
        
        while len(self.websites) > 0:
            website = self.websites.pop(0)
            if website.is_empty() != True:
                website.start_scraping()
            else:
                website = website.initialize_next_website()
            if website != None:
                self.websites.append(website)
            if len(self.websites) == 1:
                time.sleep(self.STOP_TIME)
            
        
            
      