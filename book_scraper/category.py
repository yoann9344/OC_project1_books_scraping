from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .book import Book


BASE_URL = 'https://books.toscrape.com/'


def get_all_categories_url():
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    panel_category = soup.find(id="promotions_left").find_next('div')
    ul_category = panel_category.ul.ul

    categories = {}
    for link in ul_category.find_all('a'):
        url = link['href']
        name = link.text.strip()
        categories[name] = urljoin(BASE_URL, url)

    return categories


# TODO implement _reset method
class Category():
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.index = url
        page = requests.get(url)
        self.soup = BeautifulSoup(page.text, 'html.parser')

    def iter_all_books(self):
        for name, url, _ in self.iter_all_books_url():
            book = Book(url)
            info = book.get_info()
            image = book.get_image()
            yield info, image

    def iter_all_books_url(self):
        section = self.soup.section
        for article in section.find_all('article'):
            link = article.h3.a
            name = link.text
            url = urljoin(self.url, link['href'])
            img_url = article.find('div', class_='image_container').img['src']
            img_url = urljoin(self.url, img_url)
            yield name, url, img_url

        if not self._has_reached_last_page():
            self._go_to_next_page()
            yield from self.iter_all_books_url()

    def _has_reached_last_page(self):
        try:
            self.soup.find('li', class_='next').a
            return False
        except AttributeError:
            return True

    def _go_to_next_page(self):
        url = self.soup.find('li', class_='next').a['href']
        url = urljoin(self.url, url)
        self.url = url
        page = requests.get(url)
        self.soup = BeautifulSoup(page.text, 'html.parser')


if __name__ == '__main__':
    categories = get_all_categories_url()
    assert len(categories) >= 50
    CATEGORY = 'Historical Fiction'
    category = Category(name=CATEGORY, url=categories[CATEGORY])
    assert not category._has_reached_last_page()
    category._go_to_next_page()
    assert category._has_reached_last_page()
    category = Category(name=CATEGORY, url=categories[CATEGORY])
    books_url = list(category.iter_all_books_url())
    import pprint
    print(pprint.pformat(books_url))
    assert len(books_url) >= 26
