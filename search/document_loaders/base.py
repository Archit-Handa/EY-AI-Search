from abc import ABC, abstractmethod

class DocumentLoader(ABC):
    '''Abstract base class for document loaders'''
    
    @abstractmethod
    def load(self, file_stream: str) -> str:
        '''
        Load and extract content from a document file stream
        
        @param file_stream: The file stream of the document
        @return: The extracted content
        '''
        pass