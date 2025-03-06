from abc import ABC, abstractmethod

class Store(ABC):
    '''Base class for a store'''
    
    @abstractmethod
    def add(self, documents: list[dict]) -> None:
        '''
        Add a key-value pair to the store
        
        @param key: The key to add
        @param value: The value to add
        '''
        pass
    
    @abstractmethod
    def get(self, doc_id: str) -> dict:
        '''
        Get a value from the store
        
        @param key: The key to get
        @return: The value
        '''
        pass
    
    @abstractmethod
    def delete(self, doc_id: str) -> None:
        '''
        Delete a key from the store
        
        @param key: The key to delete
        '''
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass
    
    @abstractmethod
    def search(self, query_vector: list[float], top_k: int) -> list[dict]:
        '''
        Search for a query in the store
        
        @param query: The query to search for
        @param top_k: The number of results to return
        @return: A list of keys
        '''
        pass
    
    @abstractmethod
    def close(self) -> None:
        '''Close the store'''
        pass