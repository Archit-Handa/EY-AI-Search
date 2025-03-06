from .base import Store

class VectorStore(Store):
    '''Vector Store that uses CosmosDB (MongoDB for Azure) to store embeddings'''
    
    def __init__(self):
        pass
    
    def add(self, embeddings: list[list[float]], metadatas: list[dict]):
        pass
    
    def get(self, key: str):
        pass
    
    def delete(self, key: str):
        pass
    
    def search(self, query: str, k: int):
        pass
    
    def close(self):
        pass