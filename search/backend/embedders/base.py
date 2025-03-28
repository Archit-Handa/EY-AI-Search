from abc import ABC, abstractmethod
from typing import Union

class Embedder(ABC):
    '''Base class for embedders'''
    
    def __call__(self, input: Union[str, list[str]]) -> Union[list[float], list[list[float]]]:
        '''
        Wrapper function to embed a text or a list of texts when the model is called
        
        @param input: The text or list of texts to embed
        @return: The embeddings
        '''
        if not isinstance(input, (str, list)):
            raise ValueError('Input must be a string or a list of strings')
        
        if isinstance(input, str):
            return self._embed([input])[0]
        
        return self._embed(input)
    
    @abstractmethod
    def _embed(self, input: list[str]) -> list[list[float]]:
        '''
        Embed a list of texts
        
        @param input: The list of texts to embed
        @return: The embeddings
        '''
        pass