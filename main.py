from ScraperA import ScraperA
from WebsiteA import WebsiteA
from Controller import Controller
from Website_pracuj import Website_level_1 as Website_pracuj
from scraper_pracuj import Scraper_level_1 as Scraper_pracuj
from scraper_nofluffjobs import Scraper_level_1 as Scraper_nofluff
from website_nofluffjobs import Website_level_1 as Website_nofluff

tags = []
tags.append("it")
tags.append("ds")
tags.append("staz")
tags.append("praca")

#scraperA = ScraperA()
#websiteA = WebsiteA(scraperA, tags)
scraper_pracuj = Scraper_pracuj()
website_pracuj = Website_pracuj(scraper_pracuj, tags)
scraper_nofluff = Scraper_nofluff()
website_nofluff = Website_nofluff(scraper_nofluff, tags)

websites = []
websites.append(website_pracuj)
websites.append(website_nofluff)



controller = Controller(websites)
controller.scraping()
