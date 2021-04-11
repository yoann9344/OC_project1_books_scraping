import os
import csv
from sys import exit
from signal import signal, SIGINT
from pathlib import Path
from typing import List, Dict

from tqdm import tqdm

from book_scraper import Book, Category, get_all_categories_url

FILES_PATH = 'data/'


class InterruptionHandler():
    interrupted = False

    @classmethod
    def sigint(cls, *args, **kwargs):
        cls.interrupted = True

    @classmethod
    def check_interruption(cls):
        if cls.interrupted:
            print('Excution interrupted.')
            print('Do you want to exit ? [y]/n ', end='')
            answer = input()
            if answer in ('', 'y'):
                exit(0)
            else:
                cls.interrupted = False
        return


signal(SIGINT, InterruptionHandler.sigint)


def write_image(path: Path, content: bytes):
    with path.open('wb+') as f:
        f.write(content)


def write_info(path: Path, content: List[Dict]):
    if len(content) == 0:
        return
    with path.open('w+') as f:
        dict_writer = csv.DictWriter(f, content[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(content)


categories_url = get_all_categories_url()

for name, url in categories_url.items():
    category = Category(name=name, url=url)
    path_category = Path(FILES_PATH) / name
    path_images = path_category / 'images'
    path_images.mkdir(parents=True, exist_ok=True)
    books_info = []
    with tqdm(desc=name, total=category.books_quantity()) as progress_bar:
        for info, image in category.iter_all_books():
            books_info.append(info)
            image_name = image.name.replace(os.sep, '_')
            write_image(
                path_images / f'{image_name}.{image.extension}',
                image.file,
            )
            progress_bar.update()
            InterruptionHandler.check_interruption()
    write_info(path_category / f'{name}.csv', books_info)
