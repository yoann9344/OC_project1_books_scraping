import os
import asyncio
from pathlib import Path

from tqdm import tqdm

from .pages import Book, Category
from .factories import serializer_factory, storage_factory


class Scraper():
    def __init__(self, serializer_format, service_name):
        self.serializer = serializer_factory.create(serializer_format)
        self.storage = storage_factory.create(service_name)

    async def get_book(self, book_url, path_images, book_name=None):
        book = await Book(book_url, title=book_name)
        info = book.get_info()
        image = await book.get_image()
        image_name = image.name.replace(os.sep, '_')
        self.storage.save(
            path=path_images / f'{image_name}.{image.extension}',
            data=image.file,
        )
        return info

    async def get_all_books_in_category(self, category_url, path, category_name=None):
        category = await Category(name=category_name, url=category_url)
        category_name = category_name or category.name.replace(os.sep, '_')

        path_category = Path(path) / category_name
        path_images = path_category / 'images'
        self.storage.mkdir(path_images, recursive=True)

        books_url = []
        async for book_name, url, _ in category.iter_all_books_url():
            books_url.append((book_name, url))
        tasks = []
        for book_name, book_url in books_url:
            tasks.append(
                self.get_book(book_url, path_images, book_name=book_name))

        books_info = []
        progress_bar = tqdm(total=len(books_url), desc=category_name)
        for task in asyncio.as_completed(tasks):
            info = await task
            books_info.append(info)
            progress_bar.update()
        # TODO to handle sigint, need to check if all tasks
        # are finished
        # InterruptionHandler.check_interruption()
        books_info_serialized = self.serializer.serialize(
            books_info,
            headers=books_info[0].keys(),
        )
        self.storage.save(
            path=path_category / f'{category_name}.csv',
            data=books_info_serialized,
        )

    async def get_all_books_in_all_categories(self, path):
        categories_url = await Category.get_all_categories_url()

        for category_name, category_url in categories_url.items():
            await self.get_all_books_in_category(category_name, category_url, path)
