from abc import ABC, abstractmethod
from typing import BinaryIO

class DocumentLoader(ABC):
    '''Abstract base class for document loaders'''
    
    @abstractmethod
    def load(self, file_stream: BinaryIO) -> str:
        '''
        Load and extract content from a document file stream
        
        @param file_stream: A binary file stream of the document
        @return: Extracted text content
        '''
        pass