from .base import DocumentLoader
from typing import BinaryIO

class TxtLoader(DocumentLoader):
    '''Loader for .txt files'''
    
    def load(self, file_stream: BinaryIO) -> str:
        '''Extract text from a .txt file stream'''
        return file_stream.read().decode('utf-8', errors='replace').strip()