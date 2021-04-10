import requests

from bs4 import BeautifulSoup


def get_book_info(book_url):
    page = requests.get()
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find_all('table')[0]
    informations = {}
    for tr in table.find_all('tr'):
        field_name = tr.find_all('th').first.text.lower()
        field_value = tr.find_all('td').first.text

        informations[field_name] = field_value

    # remove useless informations
    del informations['Product Type']

    print(informations)


if __name__ == '__main__':
    book_name = 'a-light-in-the-attic_1000'
    book_url = f'https://books.toscrape.com/catalogue/{book_name}/index.html'
    get_book_info(book_url)
    # {
    #     'UPC': 'a897fe39b1053632',
    #     'Product Type': 'Books',
    #     'Price (excl. tax)': 'Â£51.77',
    #     'Price (incl. tax)': 'Â£51.77',
    #     'Tax': 'Â£0.00',
    #     'Availability': 'In stock (22 available)',
    #     'Number of reviews': '0'
    # }
