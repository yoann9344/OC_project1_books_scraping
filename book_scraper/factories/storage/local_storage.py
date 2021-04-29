from io import StringIO
from pathlib import Path


class LocalStorage():
    def save(self, path: Path, data):
        if isinstance(data, bytes):
            with path.open('wb+') as f:
                f.write(data)
        elif isinstance(data, StringIO):
            with path.open('w+') as f:
                f.write(data.getvalue())

    def mkdir(self, path_images: Path, recursive=False):
        path_images.mkdir(parents=recursive, exist_ok=True)
