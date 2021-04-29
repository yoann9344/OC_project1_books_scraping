import csv
from io import StringIO


class CsvSerializer():
    def serialize(self, serialable, headers=None):
        file = StringIO()
        if not serialable:
            pass
        elif headers is None:
            self.simple_csv(file, serialable)
        else:
            self.dict_csv(file, serialable, headers)
        return file

    def simple_csv(self, serialable):
        raise NotImplementedError

    def dict_csv(self, file, serialable, headers):
        dict_writer = csv.DictWriter(file, headers)
        dict_writer.writeheader()
        dict_writer.writerows(serialable)
