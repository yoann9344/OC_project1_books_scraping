from .factory import SerializerFactory
from .csv import CsvSerializer
from .json import JsonSerializer


serializer_factory = SerializerFactory()
serializer_factory.register('csv', CsvSerializer)
serializer_factory.register('json', JsonSerializer)
# TODO implement XML
# serializer_factory.register('xml', XmlSerializer)
