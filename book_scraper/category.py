from .book import Book
from .browser import Browser


BASE_URL = 'https://books.toscrape.com/'


def get_all_categories_url():
    browser = Browser(BASE_URL)
    panel_category = browser.soup.find(id="promotions_left").find_next('div')
    ul_category = panel_category.ul.ul

    categories = {}
    for link in ul_category.find_all('a'):
        url = link['href']
        name = link.text.strip()
        categories[name] = browser.clean_url(url)

    return categories


# TODO implement _reset method
class Category(Browser):
    def __init__(self, url, name=None):
        super().__init__(url)
        if name is None:
            name = url
        self.name = name
        self.index = url

    def iter_all_books(self):
        for book_name, url, _ in self.iter_all_books_url():
            book = Book(url, name=book_name)
            info = book.get_info()
            image = book.get_image()
            yield info, image

    def iter_all_books_url(self):
        section = self.soup.section
        for article in section.find_all('article'):
            link = article.h3.a
            name = link.text
            url = self.clean_url(link['href'])
            img_url = article.find('div', class_='image_container').img['src']
            img_url = self.clean_url(img_url)
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
        self.go_to(url)

    def books_quantity(self):
        form = self.soup.find(id='promotions').find_next('form')
        strongs = form.find_all('strong')
        if len(strongs) == 3:
            total_tag, _, _ = form.find_all('strong')
        else:  # only one when 20 items or less
            total_tag = form.find_all('strong')[0]
        return int(total_tag.text)


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
