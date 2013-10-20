# encoding: utf-8
from __future__ import unicode_literals

from selenium import webdriver
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger()


class ScraperExeception(Exception):
    pass

class Scraper():
    def __init__(self):
        # Initialize a selenium browser when the class is created.
        self.browser = webdriver.PhantomJS()
        # Set the cookies by visiting base url first.
        print self.base_url
        if self.base_url:
            self.browser.get(self.base_url)

    def get_page(self, url, max_retries=3):
        # Attempts to try to get the page (retries 3 times max)
        # and turn it into a (beautiful) soup for easy parsing.
        retries = 0
        while retries < max_retries:
            try:
                logger.debug("Get -> {}".format(url))
                self.browser.get(url)
                return BeautifulSoup(self.browser.page_source)
            except:
                retries +=1
        raise ScraperExeception("Could not get the page.")

    def __exit__(self, type, value, trackback):
        self.browser.quit()
