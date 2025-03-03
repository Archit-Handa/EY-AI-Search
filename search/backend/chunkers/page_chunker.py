from .base import Chunker
from typing import Generator

class PageChunker(Chunker):
    '''Chunk a text into smaller chunks based on page breaks'''
    
    def chunk(self, text: str) -> Generator[str]:
        yield text