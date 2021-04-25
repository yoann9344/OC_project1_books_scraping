import os
import csv
import asyncio
from sys import exit
from signal import signal, SIGINT
from pathlib import Path
from typing import List, Dict

from tqdm import tqdm

from book_scraper import Book, Category

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


def write_info(path: Path, content: List[Dict], append=False):
    if content:
        with path.open('a+' if append else 'w+') as f:
            dict_writer = csv.DictWriter(f, content[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(content)


async def retrieve_book(book_url, path_images, book_name=None):
    book = await Book(book_url, title=book_name)
    info = book.get_info()
    image = await book.get_image()
    image_name = image.name.replace(os.sep, '_')
    write_image(
        path_images / f'{image_name}.{image.extension}',
        image.file,
    )
    return info


# TODO WIP
async def get_book(book_url, path_images, book_name=None):
    return await retrieve_book(book_url, path_images, book_name=book_name)


async def get_all_books():
    categories_url = await Category.get_all_categories_url()

    for category_name, category_url in categories_url.items():
        # print(category_name)
        category = await Category(name=category_name, url=category_url)
        path_category = Path(FILES_PATH) / category_name
        path_images = path_category / 'images'
        path_images.mkdir(parents=True, exist_ok=True)

        books_url = []
        async for book_name, url, _ in category.iter_all_books_url():
            books_url.append((book_name, url))
        tasks = [
        ]
        for book_name, book_url in books_url:
            tasks.append(
                retrieve_book(book_url, path_images, book_name=book_name))

        books_info = []
        progress_bar = tqdm(total=len(books_url), desc=category_name)
        for task in asyncio.as_completed(tasks):
            info = await task
            books_info.append(info)
            progress_bar.update()
        # TODO to handle sigint, need to check if all tasks
        # are finished
        # InterruptionHandler.check_interruption()
        write_info(path_category / f'{category_name}.csv', books_info)


if __name__ == '__main__':
    asyncio.run(get_all_books())
