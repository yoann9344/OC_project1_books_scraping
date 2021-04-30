# Book Scraper
Scrapes books on the best online book librairy :
https://books.toscrape.com/

## Development setup

Create a venv & activate & install the requirements.txt, then :

Unix's like:

```bash
# setup.py :
pip install --editable
getbooks
```

Windows:

```sh
reboot
```

## Usage example

Using directory option
```sh
BOOKS_DIRECTORY="plop" getbooks -c https://books.toscrape.com/catalogue/category/books/mystery_3/index.htm
export BOOKS_DIRECTORY="musics/jukebox"
getbooks -c https://books.toscrape.com/catalogue/category/books/mystery_3/index.htm
getbooks --directory plop -c https://books.toscrape.com/catalogue/category/books/mystery_3/index.htm
```

Retrieve all books
```sh
getbooks
getbooks --all
```

Retrieve all books of one category
```sh
getbooks -c <url_category>
getbooks --category <url_category>
```

Retrieve one book
```sh
getbooks -b <url_category>
getbooks --book <url_book>
```

Retrieve all books, with data in json format
```sh
getbooks --json
getbooks --all --json
```

You can send SIGINT to interrupt the execution of the programm (CTRL + C)

## Meta

Distributed under the HaveFun license. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/yoann9344/OC_project1_books_scraping/fork>)
