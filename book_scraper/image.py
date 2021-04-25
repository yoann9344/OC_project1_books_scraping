from dataclasses import dataclass


@dataclass
class Image():
    """Contains the logic to retrieve book's page's content
    Attributes
    -------
    file: bytes
        The image
    name: str
        name of the image
    extension: str
        Image's extension type
    """
    file: bytes
    name: str
    extension: str
