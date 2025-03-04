from .base import Chunker
from typing import Generator

class SentenceChunker(Chunker):
    '''Chunk a text into smaller chunks based on sentence breaks '.' (full stops)'''
    
    def chunk(self, text: str) -> Generator[str, None, None]:
        for sent in text.split('.'):
            yield sent