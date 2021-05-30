import re

from ..browser import Browser


class Thing(Browser):
    """Contains the logic to retrieve something on a page
    Methods
    -------
    get_info()
        Retrieve thing's inforations
    Attributes
    ----------
    headers: set
        all keys of informations
    """
    headers = [
        'title',
        'url',
        'Capital Social',
        'Numéro TVA Intercommunautaire',
    ]

    async def __init__(self, url, title=None):
        await super().__init__(url)
        self.url = url
        self._title = title

    def get_info(self):
        """Retrieve the thing's informations
        Returns
        -------
        informations: dict
        """
        informations = {}

        informations['title'] = self.title
        informations['url'] = self.url
        informations['Capital Social'] = self.soup.find(id='capital-histo-description').text
        informations['Numéro TVA Intercommunautaire'] = self.soup.find(id='tva_number').text

        headers = Thing.headers[:]
        # extract info
        table = self.soup.find(id='rensjur')
        for field_name, field_value in self._iter_table(table):
            informations[field_name] = field_value
            headers.append(field_name)
        table = self.soup.find(id='chiffrecle')
        for field_name, field_value in self._iter_table_with_headers(table):
            informations[field_name] = field_value
            headers.append(field_name)
        Thing.headers = list(dict.fromkeys(headers))
        self.parse_info(informations)

        return informations

    @property
    def title(self):
        """Retrieve the thing's title
        Returns
        -------
        title: str
        """
        if title := getattr(self, '_title', None):
            return title
        else:
            return self.soup.find(id='identite_deno').text

    def _iter_table_with_headers(self, table):
        headers = []
        for th in table.find_all('th'):
            headers.append(th.text)

        for tr in table.find_all('tr'):
            # name and value
            tds = tr.find_all('td')
            if len(tds) == len(headers):
                name = tds[0].text
                for i, td in enumerate(tds):
                    if i == 0:
                        continue
                    yield name + headers[i], td.text

    def _iter_table(self, table):
        """Iterate on the table containing product informations
        Yields
        -------
        name: str
            information's name
        value: str
            corresponding value
        """
        for tr in table.find_all('tr'):
            # name and value
            tds = tr.find_all('td')
            if len(tds) == 2:
                name = tds[0].text
                value = tds[1].text
                if name:
                    yield name, value

    def parse_info(self, info):
        replace_copier_le = re.compile(r'Copier le n° de \w+')
        for key, value in info.items():
            value = replace_copier_le.sub('', value)
            # removes blank lines
            value = "".join(
                [s.strip() for s in value.strip().splitlines(True) if s.strip()])
            info[key] = value


if __name__ == '__main__':
    book_name = 'a-light-in-the-attic_1000'
    book_url = f'https://books.toscrape.com/catalogue/{book_name}/index.html'
    book = Thing(book_url)

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
