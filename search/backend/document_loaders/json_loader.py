import json
from .base import DocumentLoader
from typing import BinaryIO

class JsonLoader(DocumentLoader):
    '''Loader for .json files'''
    
    def load(self, file_stream: BinaryIO) -> str:
        '''Extract content from a .json file stream'''
        return json.dumps(json.load(file_stream), indent=4)