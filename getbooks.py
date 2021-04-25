import re

from book_scraper import get

import click


# TODO WIP
@click.command()
@click.option('-d', '--directory', envvar='BOOKS_DIRECTORY', default='./data/')
@click.option(
    '-b', '--book', 'book_url', type=str,
)
@click.option(
    '-c', '--category', 'category_url', type=str,
)
def cli(directory, book_url, category_url):
    if not (book_url is None) ^ (category_url is None):
        print('Requiert : -c ou -b')
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

    if book_url is not None:
        if not url_pattern.match(book_url):
            print('Invalid url for book')
            return
    elif category_url is not None:
        if not url_pattern.match(category_url):
            print('Invalid url for category')
            return
    click.echo('Directory %s' % directory)
    click.echo('book_url %s' % book_url)
    click.echo('category_urltegory %s' % category_url)
