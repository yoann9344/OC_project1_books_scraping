import re
import sys
import asyncio
from pathlib import Path
from signal import signal, SIGINT

from book_scraper import Scraper, InterruptionHandler

import click


signal(SIGINT, InterruptionHandler.sigint)


@click.command()
@click.option('-a', '--all', 'all_books', is_flag=True)
@click.option('-b', '--book', 'book_url', type=str)
@click.option('-c', '--category', 'category_url', type=str)
@click.option('-d', '--directory', envvar='BOOKS_DIRECTORY', default='./data/')
def cli(directory, book_url, category_url, all_books):
    if book_url and category_url:
        print('Can\'t use -c and -b together.', file=sys.stderr)
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        return
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    scraper = Scraper('csv', 'local')
    path = Path(directory)
    scraper.storage.mkdir(path, recursive=True)

    if book_url:
        if not url_pattern.match(book_url):
            print('Invalid url for book.', file=sys.stderr)
            return
        asyncio.run(scraper.get_book(book_url, path))
    elif category_url:
        if not url_pattern.match(category_url):
            print('Invalid url for category.', file=sys.stderr)
            return
        asyncio.run(scraper.get_all_books_in_category(category_url, path))
    else:
        print('all')
        asyncio.run(scraper.get_all_books_in_all_categories(path))
