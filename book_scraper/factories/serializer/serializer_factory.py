from book_scraper.factories.factory import Factory


class SerializerFactory(Factory):
    required_attributes = ['serialize', 'extension']
