import json


class FileHandler:
    def __init__(self, filename="log.json"):
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    def save(self, data):
        try:
            with open(self._filename, "w") as file:
                json.dump(data, file, indent=4)
        except OSError as error:
            print("Log can't be saved: ", error)
