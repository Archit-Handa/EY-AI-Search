from abc import ABC, abstractmethod
from typing import Generator

class Chunker(ABC):
    '''Abstract base class for chunkers'''
    
    @abstractmethod
    def chunk(self, text: str) -> Generator[str]:
        '''
        Chunk a text into smaller chunks
        
        @param text: The text to chunk
        @return: A generator of chunks
        '''
        pass