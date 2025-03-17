from .base import Chunker
import re
from typing import Iterator

class ParagraphChunker(Chunker):
    '''Chunk a text into smaller chunks based on paragraph breaks'''
    def __init__(self):
        self.paragraph_break = '\n'
    
    def chunk(self, text: str) -> Iterator[str]:
        '''Yield text chunks split by paragraph breaks'''
        paragraph_pattern = re.compile(r'(?<=[.!?])\n+')
        return filter(None, map(str.strip, paragraph_pattern.split(text)))