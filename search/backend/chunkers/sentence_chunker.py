from .base import Chunker
from typing import Iterator
import re

class SentenceChunker(Chunker):
    '''Chunk a text into smaller chunks based on sentence breaks - period (.), exclamation mark (!), question mark (?)'''
    
    def chunk(self, text: str) -> Iterator[str]:
        '''Yield sentences as individual chunks'''
        sentence_pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s+')
        return filter(None, map(str.strip, sentence_pattern.split(text)))