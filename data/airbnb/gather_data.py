# encoding: utf-8
from __future__ import unicode_literals

from models import AirbnbListing
from utils.scraper import Scraper
from utils.logger import get_logger
from utils.helpers import clean_string, extract_digits, data_attribute

import re

logger = get_logger()


class AirbnbScraper(Scraper):
    """
    Get's all AirBNB listings in DC.
    """

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
            logger.info("Retriving info about from {} [{}/{}]".format(link, count, len(listing_links)))
            try:
                data = self.scrap_listing(link)
                AirbnbListing.create(**data)
            except Exception as e:
                logger.error(e)
            count += 1


if __name__ == '__main__':
    airbnb = AirbnbScraper()
    airbnb.scrap_and_store()
