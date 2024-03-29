import json
from io import StringIO


class JsonSerializer():
    extension = 'json'

    def serialize(self, serialable, headers=None):
        file = StringIO()
        if not serialable:
            pass
        else:
            json.dump(serialable, file)
        return file
