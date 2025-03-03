import json
from .base import DocumentLoader

class JsonLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        print(file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            print(file)
            return json.load(file)