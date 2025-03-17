from .base import Chunker
from typing import Iterator

class FixedSizeChunker(Chunker):
    '''Chunk a text into smaller chunks of a fixed size'''
    def __init__(self, chunk_size: int = 200):
        if chunk_size <= 0:
            raise ValueError("Chunk size must be a positive integer.")
        
        self.chunk_size = chunk_size
    
    def chunk(self, text: str) -> Iterator[str]:
        '''Yiwld fixed-size chunks from the input text'''
        return (text[i : i + self.chunk_size] for i in range(0, len(text), self.chunk_size))