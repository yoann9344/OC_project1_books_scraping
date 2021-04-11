import os
import csv
from pathlib import Path
from typing import List, Dict

from book_scraper import Book, Category, get_all_categories_url

FILES_PATH = 'data/'


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
    print('Category :', name)
    category = Category(name=name, url=url)
    path_category = Path(FILES_PATH) / name
    path_images = path_category / 'images'
    path_images.mkdir(parents=True, exist_ok=True)
    books_info = []
    for info, image in category.iter_all_books():
        books_info.append(info)
        image_name = image.name.replace(os.sep, '_')
        write_image(
            path_images / f'{image_name}.{image.extension}',
            image.file,
        )
    write_info(path_category / f'{name}.csv', books_info)
