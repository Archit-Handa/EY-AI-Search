from .base import Chunker
from typing import Generator

class FixedSizeChunker(Chunker):
    '''Chunk a text into smaller chunks of a fixed size'''
    def __init__(self, chunk_size: int = 200):
        self.chunk_size = chunk_size
    
    def chunk(self, text: str) -> Generator[str, None, None]:
        for i in range(0, len(text), self.chunk_size):
            yield text[i: i+self.chunk_size]