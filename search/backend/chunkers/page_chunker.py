from .base import Chunker
from typing import Iterator

class PageChunker(Chunker):
    '''Chunk a text into smaller chunks based on page breaks'''
    def __init__(self):
        self.page_break = '\f'
    
    def chunk(self, text: str) -> Iterator[str]:
        '''Yield text chunks split by page breaks'''
        return filter(None, text.split(self.page_break))