from ..factory import Factory


class StorageFactory(Factory):
    def validate(self, builder):
        required_methods = ['save', 'mkdir']
        for method in required_methods:
            if not hasattr(builder, method):
                raise NotImplementedError(
                    f'Serializer\'s method "{method}" not implemented'
                )
