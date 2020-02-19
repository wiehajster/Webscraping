from abc import ABC,abstractmethod
import requests 
import pandas as pd
import re

class Scraper(ABC):
    
    def __init__(self):
        pass
    
    def scrape(self, url):
        response = requests.get(url)
        return response
    
    def concat_all_strings(self, item, delim, other_types):
    
        concatenated_string = ''
        if isinstance(item, list) or isinstance(item, tuple) or isinstance(item, dict) or isinstance(item, pd.Series):

            for i in item:
                if isinstance(item, dict):
                    if isinstance(item[i], bool) and item[i] == True:                       
                        to_concat = self.concat_all_strings(i, delim, other_types)
                    else:
                        to_concat = self.concat_all_strings(item[i], delim, other_types)
                else:
                    to_concat = self.concat_all_strings(i, delim, other_types)
                if len(to_concat):
                    concatenated_string += to_concat + delim
        elif other_types == False:
            if isinstance(item, str):
                return item
        else:
            return str(item)

        return concatenated_string[: -1]
    
    def remove_from_tags(self, item, items_to_remove):
        for i in items_to_remove:
            item = re.sub(i, '', item)
            item = re.sub('\|\|','|',item)
        return item