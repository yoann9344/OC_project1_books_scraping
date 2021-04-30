from ..factory import Factory


class StorageFactory(Factory):
    required_attributes = ['save', 'mkdir']
