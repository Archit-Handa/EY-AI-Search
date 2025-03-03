from .base import DocumentLoader

class TxtLoader(DocumentLoader):
    '''Loader for .txt files'''
    
    def load(self, file_stream: str) -> str:
        return file_stream.read().decode("utf-8").strip()