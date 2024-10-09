import os

class FileHandler:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def write_to_file(self, data: str) -> None:
        try:
            with open(self.file_path, 'w') as file:
                file.write(data)
            print("Data written successfully.")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def read_from_file(self) -> str:
        try:
            if not os.path.exists(self.file_path):
                print("File does not exist.")
                return ""
                
            with open(self.file_path, 'r') as file:
                return file.read()
        except IOError as e:
            print(f"Error reading from file: {e}")
            return ""
