import os


class File:
    def __init__(self, file_name):
        # Check if the file exists
        if os.path.exists(file_name):
            # Open the file in read/write mode
            self.file = open(file_name, 'r+')
        else:
            # Create the file if it doesn't exist
            self.file = open(file_name, 'w')

    def __enter__(self):
        # Return the File object
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Do nothing
        pass

    def __del__(self):
        # Close the file in the destructor
        self.file.close()

    def write(self, data):
        # Write the data to the file
        self.file.write(data)

    def clear(self):
        # Clear the file
        self.file.seek(0)
        self.file.truncate()
