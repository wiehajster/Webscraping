from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import ast

def scrape_level_1(response):
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    last_page_nr = soup.find_all('li', class_='pagination_element-page')[-1]
    last_page_nr = int(last_page_nr.text)
    
    return last_page_nr

def scrape_level_2(response):
    bs = BeautifulSoup(response.text, 'lxml')
    soup = response.text
    start = re.search(r'window.__INITIAL_STATE__ = ', soup)
    end = re.search(';\s*var __RAWURL__ = ', soup)
    
    
    json = soup[start.end(): end.start()]
    json = re.sub('true', 'True', json)
    json = re.sub('false', 'False', json)
    print(json)
    d = ast.literal_eval(json)
    '''
    df = pd.DataFrame()
    df['offerId'] = d['commonOfferId']
    df['title'] = d['jobTitle']
    df['website'] = 'pracuj'
    
    df['url'] = ''
    df['company'] = d['employer']
    df['country'] = d['countryName']
    df['city'] = 
    '''
    return pd.DataFrame(d['offers'])


    '''
    items = soup.find_all('li', class_='results__list-container-item')
    
    titles = []
    company_names = []
    descriptions = []
    offer_urls = []
    company_urls = []
    
    base_url = 'https://www.pracuj.pl/'
    
    for item in items:
        job = item.find('a', class_='offer-details__title-link')
        print(job)
        titles.append(job.text)
        offer_urls.append(base_url + job['href'])
        
    df = pd.DataFrame({'Title': titles, 'OfferUrl': offer_urls})
    return df
    '''

if __name__ == '__main__':
    url = 'https://www.pracuj.pl/praca'
    response = requests.get(url)
    
    last_page_nr = scrape_level_1(response)
    
    new_urls = []
    base_url = 'https://www.pracuj.pl/praca/ds;kw?pn='
    
    for i in range(1, last_page_nr + 1):
        new_urls.append(base_url + str(i))
    
    results = []
    item = {}
    for url in new_urls:
        response = requests.get(url)
        item = scrape_level_2(response)
        results.append(item)
        break
        
    final_df = pd.concat(results)
    #final_df.to_excel('results.xlsx', index=False)