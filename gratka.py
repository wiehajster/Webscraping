from Scraper import Scraper
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

class Gratka_Initial_Scraper(Scraper):

    def scrape(self, url):
        response = super().scrape(url)
        soup = BeautifulSoup(response.text, 'lxml')
    
        try:
            last_page_nr = soup.find('div', class_='pagination').find('input')['max']
            last_page_nr = int(last_page_nr)
        except (TypeError, AttributeError):
            return 1
        
        return last_page_nr
    
class Gratka_Actual_Scraper(Scraper):
    
    def scrape(self, url):
        response = super().scrape(url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        items = soup.find_all('div', class_='teaser__content')
        
        titles = []
        urls = []
        addresses=[]
        number_of_rooms = []
        sizes = []
        prices = []
        
        for item in items:
            url = item.find('a')['href']
            title = item.find('a').text
            address = item.find('span', class_='teaser__region').previous_sibling
            address = re.sub('\s+', ' ', str(address))
            address = re.sub('^\s+', '', re.sub(',?\s+$', '', address))
            
            params = item.find('ul', class_='teaser__params')
            try:
                n_rooms = re.search('(?<=iczba pokoi:)\s*\d+', params.text).group()
                n_rooms = int(n_rooms)
            except AttributeError:
                n_rooms = np.nan
            try:
                size = re.search('owierzchnia[^:]*:\s*[\d.]+', params.text).group()
                size = re.sub('[^:]+:\s*', '', size)
                size = float(size)
            except AttributeError:
                size = np.nan
                
            price = item.find('p', class_='teaser__price').text
            price = re.search('[\d ]+', price).group()
            price = re.sub('\s', '', price)
            price = int(price)
            
            titles.append(title)
            urls.append(url)
            addresses.append(address)
            number_of_rooms.append(n_rooms)
            sizes.append(size)
            prices.append(price)
            
        return pd.DataFrame({'Title': titles, 'Url': urls, 'Address': addresses,
                             'NumberOfRooms': number_of_rooms, 'Size': sizes,
                             'Price': prices, 'Source': 'gratka'})
'''    
if __name__ == '__main__':
    distance = 50
    page_nr = 1
    city_name = 'kielce'
    base_url = f'https://gratka.pl/nieruchomosci/mieszkania/{city_name}/wynajem'
    
    scraper1 = Gratka_Initial_Scraper()
    nr = scraper1.scrape(base_url)
    
    urls = []
    for i in range(1, nr+1):
        url = base_url + f'?page={i}'
        urls.append(url)
        
    scraper2 = Gratka_Actual_Scraper()
    df = scraper2.scrape(base_url)

    dfs = []
    count = 0
    for url in urls:
        print(count / len(urls))
        count += 1
        df = scraper2.scrape(url)
        dfs.append(df)
        
    df = pd.concat(dfs)
'''    
