import json

from .File import File


class JSONFile(File):
    def __init__(self, file_name):
        # Call the parent class's __init__() method
        super().__init__(file_name)

        # Try to parse the JSON data from the file
        try:
            self.json_data = json.load(self.file)
        except:
            # Set the json_data attribute to an empty dictionary if the operation fails
            self.json_data = {}

        self.usePretty = False
        self.pretty = {
            "sort_keys": True,
            "indent": 4,
        }

    def __del__(self):
        # save the file
        self.save()
        # call the parent class's __del__() method
        super().__del__()

    def update(self, data):
        # Update the JSON data with the new data
        try:
            self.json_data.update(data)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            self.json_data = data

        # call save
        self.save()

    def save(self):
        # save the changes to the file
        file_name = self.file.name
        with File(file_name) as original_file:
            # clear the file
            original_file.clear()
            json.dump(
                self.json_data,
                original_file.file,
                **self.pretty if self.usePretty else {}
            )

    def make_pretty(self, indent=4, sort_keys=True):
        self.pretty = {
            "sort_keys": sort_keys,
            "indent": indent,
        }
        self.usePretty = True

    def make_ugly(self):
        self.usePretty = False
