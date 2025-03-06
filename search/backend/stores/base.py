from abc import ABC, abstractmethod

class Store(ABC):
    '''Base class for a store'''
    
    @abstractmethod
    def add(self, key: str, value: str) -> None:
        '''
        Add a key-value pair to the store
        
        @param key: The key to add
        @param value: The value to add
        '''
        pass
    
    @abstractmethod
    def get(self, key: str) -> str:
        '''
        Get a value from the store
        
        @param key: The key to get
        @return: The value
        '''
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        '''
        Delete a key from the store
        
        @param key: The key to delete
        '''
        pass
    
    @abstractmethod
    def search(self, query: str, top_k: int) -> list[str]:
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