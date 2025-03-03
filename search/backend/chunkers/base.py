from abc import ABC, abstractmethod

class Chunker(ABC):
    '''Abstract base class for chunkers'''
    
    @abstractmethod
    def chunk(self, text: str) -> list[str]:
        '''
        Chunk a text into smaller chunks
        
        @param text: The text to chunk
        @return: The list of chunks
        '''
        pass