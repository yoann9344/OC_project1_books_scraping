import re

import requests

from .browser import Browser
from .image import Image


UPC = 'UPC'
PRODUCT_TYPE = 'Product Type'
PRICE_WITHOUT_TAX = 'Price (excl. tax)'
PRICE = 'Price (incl. tax)'
TAX = 'Tax'
AVAILABILITY = 'Availability'
REVIEWS = 'Number of reviews'


class Book(Browser):
    def __init__(self, url, name=None):
        super().__init__(url)
        if name is None:
            name = url
        self.name = name

    def get_info(self):
        informations = {}
        for field_name, field_value in iter_table(self.soup.table):
            informations[field_name] = field_value

        return extract_info(informations)

    def get_image(self):
        """Retrieve the book's image
        Returns
        -------
        bytes, str
            book's image and extension's name
        """
        img_url = self.soup.find(id='product_gallery').img['src']
        img_url = self.clean_url(img_url)
        image = requests.get(img_url).content
        image_extension = img_url.split('.')[-1]
        return Image(file=image, name=self.name, extension=image_extension)


def iter_table(soup_table):
    for tr in soup_table.find_all('tr'):
        yield tr.th.text, tr.td.text


def extract_info(info):
    """Extract the required book's informations
    Parameters
    ----------
    info:  dict
         All extracted informations

    Returns
    -------
    dict
        parsed book's informations
    """
    extracted_info = {}

    extracted_info[UPC] = info[UPC]
    extracted_info[PRICE_WITHOUT_TAX] = float(info[PRICE_WITHOUT_TAX][2:])
    extracted_info[PRICE] = float(info[PRICE][2:])
    extracted_info[TAX] = float(info[TAX][2:])

    m = re.search(r'\d+', info[AVAILABILITY])
    extracted_info[AVAILABILITY] = int(m.group(0))
    extracted_info[REVIEWS] = int(info[REVIEWS])

    return extracted_info


if __name__ == '__main__':
    book_name = 'a-light-in-the-attic_1000'
    book_url = f'https://books.toscrape.com/catalogue/{book_name}/index.html'
    book = Book(book_url)

    info = book.get_info()
    value_set = {
        'UPC': 'a897fe39b1053632',
        'Price (excl. tax)': 51.77,
        'Price (incl. tax)': 51.77,
        'Tax': 0.0,
        'Availability': 22,
        'Number of reviews': 0,
    }
    assert info == value_set

    image = book.get_image()
    assert isinstance(image, bytes)
