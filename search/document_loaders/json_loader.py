import json
from .base import DocumentLoader

class JsonLoader(DocumentLoader):
    def load(self, file_stream: str) -> str:
        data = json.load(file_stream)
        return json.dumps(data, indent=4)