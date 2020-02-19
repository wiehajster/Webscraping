from ScraperA import ScraperA
from WebsiteA import WebsiteA
from Controller import Controller
from Website_pracuj import Website_level_1
from scraper_pracuj import Scraper_level_1

tags = []
tags.append("it")
tags.append("ds")
tags.append("staz")
tags.append("praca")

#scraperA = ScraperA()
#websiteA = WebsiteA(scraperA, tags)
scraper_pracuj = Scraper_level_1()
website_pracuj = Website_level_1(scraper_pracuj, tags)

websites = []
websites.append(website_pracuj)

controller = Controller(websites)
controller.scraping()
