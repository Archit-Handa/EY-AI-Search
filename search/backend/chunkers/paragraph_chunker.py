from .base import Chunker
from typing import Iterator

class ParagraphChunker(Chunker):
    '''Chunk a text into smaller chunks based on paragraph breaks'''
    def __init__(self, paragraph_break: str='\n\n'):
        self.paragraph_break = paragraph_break
    
    def chunk(self, text: str) -> Iterator[str]:
        '''Yield text chunks split by paragraph breaks'''
        return filter(None, map(str.strip, text.split(self.paragraph_break)))