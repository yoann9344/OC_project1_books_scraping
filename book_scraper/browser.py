from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class Browser():
    def __init__(self, name, url):
        self.url = url
        page = requests.get(url)
        self.soup = BeautifulSoup(page.text, 'html.parser')

    def go_to(self, url):
        url = self.clean_url(url)
        page = requests.get(url)
        self.soup = BeautifulSoup(page.text, 'html.parser')

    def clean_url(self, url_to_clean):
        return urljoin(self.url, url_to_clean)
