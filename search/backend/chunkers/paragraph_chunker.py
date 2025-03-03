from .base import Chunker
from typing import Generator

class ParagraphChunker(Chunker):
    '''Chunk a text into smaller chunks based on paragraph breaks'''
    
    def chunk(self, text: str) -> Generator[str, None, None]:
        for para in text.split('\n\n'):
            yield para