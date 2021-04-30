class Factory:
    def __init__(self):
        self._builders = {}

    def register(self, name, builder):
        self.validate(builder)
        self._builders[name] = builder

    def create(self, name, *args, **kwargs):
        builder = self._builders.get(name)
        if not builder:
            raise ValueError(name)
        return builder(*args, **kwargs)

    def validate(self, builder):
        for method in self.required_attributes:
            if not hasattr(builder, method):
                raise NotImplementedError(
                    f'Serializer\'s method "{method}" not implemented'
                )
