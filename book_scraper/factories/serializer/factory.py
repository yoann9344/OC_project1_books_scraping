from book_scraper.factories.factory import Factory


class SerializerFactory(Factory):
    def validate(self, builder):
        required_methods = ['serialize']
        for method in required_methods:
            if not hasattr(builder, method):
                raise NotImplementedError(
                    f'Serializer\'s method "{method}" not implemented'
                )
