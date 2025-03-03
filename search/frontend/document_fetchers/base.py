from abc import ABC, abstractmethod
from typing import Union, Tuple
from io import BytesIO

class DocumentFetcher(ABC):
    '''Abstract base class for document fetchers'''
    
    @abstractmethod
    def fetch_document(self) -> Union[Tuple[str, BytesIO], None]:
        '''
        Fetch and return a document
        
        @return: The document
        '''
        pass