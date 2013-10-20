# encoding: utf-8
from __future__ import unicode_literals

from selenium import webdriver
from bs4 import BeautifulSoup
from models import AirbnbListing
from utils import clean_string, extract_digits, get_logger
import csv
import re

logger = get_logger()

class Scraper():
    def __init__(self):
        # Initialize a selenium browser when the class is created.
        self.browser = webdriver.PhantomJS()
        # Set the cookies by visiting base url first.
        print self.base_url
        if self.base_url:
            self.browser.get(self.base_url)

    def get_page(self, url):
        retries = 0
        while retries < 3:
            try:
                logger.info("Get -> {}".format(url))
                self.browser.get(url)
                return BeautifulSoup(self.browser.page_source)
            except:
                retries +=1
        return None

    def __exit__(self, type, value, trackback):
        self.browser.quit()


def data_attribute(soup, attr):
    element = soup.find(attrs={attr: re.compile('')})
    if element:
        return element.get(attr)
    else:
        return None

class AirbnbScraper(Scraper):
    base_url = "https://www.airbnb.co.uk"
    def get_listings(self):
        url = "https://www.airbnb.co.uk/s/Washington-DC"
        listing_links = []
        while url:
            soup = self.get_page(url)
            rooms = soup.select('.room_title a')
            logger.info("Found {} listings".format(len(rooms)))
            for room in rooms:
                listing_links.append("https://www.airbnb.co.uk{}".format(room.get('href')))
            # Check if there is a 'next page' link.
            next = soup.select(".next a")
            if next:
                url = "https://www.airbnb.co.uk{}".format(next[0].get('href'))
            else:
                url = None
            self.browser.save_screenshot('test.png')
        return listing_links

    def find_detail(self, soup, text):
        try:
            return clean_string(
                soup.find("td", text=re.compile(text)).find_next('td').text)
        except:
            return None

    def scrap_listing(self, url):
        soup = self.get_page(url)
        location = soup.select("#street-view #pano")[0]
        price = soup.select("#price_amount")[0].text
        description = soup.select("#description_text_wrapper")[0].text
        airbnb_id = int(url.replace('https://www.airbnb.co.uk/rooms/', ''))
        neighbourhood = data_attribute(soup, 'data-neighborhood-id')
        bedrooms = extract_digits(self.find_detail(soup, "Bedrooms:"))
        try:
            accommodates = extract_digits(self.find_detail(soup, "Accommodates:"))
        except:
            accommodates = bedrooms
        try:
            bathrooms = extract_digits(self.find_detail(soup, "bathrooms:"))
        except:
            bathrooms = None

        data = {
            'airbnb_id': airbnb_id,
            'neighbourhood': neighbourhood,
            'description':  clean_string(description),
            'latitude': location.get('data-lat'),
            'longitude': location.get('data-lng'),
            'room_type': self.find_detail(soup, "Room type:"),
            'bed_type': self.find_detail(soup, "Bed type:"),
            'bedrooms':  bedrooms,
            'bathrooms': bathrooms,
            'accommodates': accommodates,
            'price': extract_digits(price),
        }
        return data

    def scrap_and_store(self):
        listing_links = self.get_listings()
        count = 0
        for link in listing_links:
            logger.info("Scraping [{}/{}]".format(count, len(listing_links)))
            try:
                data = self.scrap_listing(link)
                AirbnbListing.create(**data)
            except Exception as e:
                logger.error(e)
            count += 1


def create_csv():
    airbnb_listings = AirbnbListing.select()
    f = open('airbnb.csv', 'wb')
    keys = airbnb_listings[0].as_dict().keys()
    csv_file = csv.DictWriter(f, keys)
    csv_file.writeheader()
    for airbnb in airbnb_listings:
        csv_file.writerow(airbnb.as_dict())


if __name__ == '__main__':
    #airbnb = AirbnbScraper()
    #airbnb.scrap_and_store()
    create_csv()
