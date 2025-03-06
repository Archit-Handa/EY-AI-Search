from .base import Store
from dotenv import load_dotenv
import pymongo
import os
import uuid

load_dotenv()

class VectorStore(Store):
    '''Vector Store that uses CosmosDB (MongoDB for Azure) to store embeddings'''
    
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('COSMOSDB_CONNECTION_STRING'))
        self.db = self.client[os.getenv('COSMOSDB_DATABASE_NAME')]
        self.collection = self.db['embeddings']
    
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