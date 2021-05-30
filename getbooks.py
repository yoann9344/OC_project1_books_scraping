import csv as csv_reader
import asyncio
from pathlib import Path
from signal import signal, SIGINT

from book_scraper import Scraper, InterruptionHandler

import click


signal(SIGINT, InterruptionHandler.sigint)


@click.command()
@click.argument('urls_file', type=click.File('r'))
@click.option('-d', '--directory', envvar='SCRAPER_DIRECTORY', default='.')
@click.option('--csv', is_flag=True)
@click.option('--json', is_flag=True)
@click.option('--docx', is_flag=True)
def cli(directory, urls_file, csv, json, docx):
    # if :
    #     print('Can\'t use -c, -b and all together.', file=sys.stderr)
    #     ctx = click.get_current_context()
    #     click.echo(ctx.get_help())
    #     return
    # url_pattern = re.compile(
    #     r'^(?:http|ftp)s?://'  # http:// or https://
    #     r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
    #     r'localhost|'  # localhost
    #     r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
    #     r'(?::\d+)?'  # optional port
    #     r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # formats = {
    #     'csv': csv,
    #     'json': json,
    #     'docx': docx,
    # }
    format_type = 'csv'
    storage_type = 'local'
    scraper = Scraper(format_type, storage_type)
    path = Path(directory)
    scraper.storage.mkdir(path, recursive=True)

    things_urls = []
    for row in csv_reader.reader(urls_file):
        things_urls.append(row)

    asyncio.run(scraper.get_all_things_from_url_list(things_urls, path))
