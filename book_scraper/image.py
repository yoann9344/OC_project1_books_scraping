from dataclasses import dataclass


@dataclass
class Image():
    file: bytes
    name: str
    extension: str
