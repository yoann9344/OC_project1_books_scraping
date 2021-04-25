import re

from ..browser import Browser
from ..models import Image


UPC = 'UPC'
PRODUCT_TYPE = 'Product Type'
PRICE_WITHOUT_TAX = 'Price (excl. tax)'
PRICE = 'Price (incl. tax)'
TAX = 'Tax'
AVAILABILITY = 'Availability'
REVIEWS = 'Number of reviews'
RATING_CLASSES = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five']


class Book(Browser):
    """Contains the logic to retrieve book's page's content
    Methods
    -------
    get_info()
        Retrieve book's inforations
    get_image()
        Retrieve image, returns the Image's dataclass
    """
    async def __init__(self, url, title=None, category=None):
        await super().__init__(url)
        self.url = url
        self._title = title
        self._category = category

    def get_info(self):
        """Retrieve the book's description
        Returns
        -------
        informations: dict
        """
        informations = {}

        # extract product info
        for field_name, field_value in self._iter_product_info():
            informations[field_name] = field_value
        informations = self.parse_product_info(informations)

        informations['title'] = self.title
        informations['url'] = self.url
        informations['image_url'] = self.image_url
        informations['rating'] = self.get_rating()
        informations['category'] = self.category_name
        informations['description'] = self.get_description()

        return informations

    def get_description(self):
        """Retrieve the book's description
        Returns
        -------
        description: str
        """
        description_title = self.soup.find(id='product_description')
        # Sometimes books have no description
        if description_title is None:
            return ''
        else:
            return description_title.find_next('p').text

    def get_rating(self):
        """Retrieve the book's rating or 0
        Returns
        -------
        rating: int
        """
        stars = self.soup.find('p', class_='star-rating')
        for index, class_number in enumerate(RATING_CLASSES):
            if class_number in stars.attrs['class']:
                return index
        else:
            return 0

    @property
    def category_name(self):
        """Retrieve the book's category
        Returns
        -------
        category_name: str
        """
        if category := getattr(self, '_category', None):
            return category
        else:
            bread = self.soup.find('ul', class_='breadcrumb')
            _, _, category_link = bread.find_all('a')
            self._category = category_link.text
            return self._category

    @property
    def title(self):
        """Retrieve the book's title
        Returns
        -------
        title: str
        """
        if title := getattr(self, '_title', None):
            return title
        else:
            article = self.soup.find('article', class_='product_page')
            self._title = article.find('h1').text
            return self._title

    @property
    def image_url(self):
        """Retrieve the book's image's url
        Returns
        -------
        image_url: str
        """
        if url := getattr(self, '_image_url', None):
            return url
        else:
            self._image_url = self.soup.find(id='product_gallery').img['src']
            return self._image_url

    async def get_image(self):
        """Retrieve the book's image
        Returns
        -------
        image: Image
            book's image using Image's dataclass
        """
        # image_response = await self.get(self.img_url)
        # image = image_response.content
        image = (await self.get(self.image_url)).content
        image_extension = self.image_url.split('.')[-1]
        return Image(file=image, name=self.title, extension=image_extension)

    def _iter_product_info(self):
        """Iterate on the table containing product informations
        Yields
        -------
        name: str
            information's name
        value: str
            corresponding value
        """
        for tr in self.soup.table.find_all('tr'):
            # name and value
            yield tr.th.text, tr.td.text

    @staticmethod
    def parse_product_info(info):
        """Parse the required book's informations
        Parameters
        ----------
        info: dict
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
