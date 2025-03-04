from .base import Chunker
from typing import Generator
import re

class SentenceChunker(Chunker):
    '''Chunk a text into smaller chunks based on sentence breaks - period (.), exclamation mark (!), question mark (?)'''
    
    def chunk(self, text: str) -> Generator[str, None, None]:
        for sent in re.split(r'([.!?])\s*', text):
            if sent not in ['', '.', '!', '?']: yield sent