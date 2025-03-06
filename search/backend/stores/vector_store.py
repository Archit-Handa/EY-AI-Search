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
    
    def add(self, documents: list[dict]) -> None:
        for doc in documents:
            doc['id'] = str(uuid.uuid4())
            doc.setdefault('metadata', {})
            
        self.collection.create_indexes([
            {
                'name': 'vector_index',
                'key': [('vector', 'vector')],
                'type': 'vectorSearch',
                'similarity': 'cosine',
                'algorihtm': 'HNSW'
            }
        ])
        
        self.collection.insert_many(documents)
    
    def get(self, doc_id: str) -> dict:
        return self.collection.find_one({'id': doc_id}, {'_id': 0})
    
    def delete(self, doc_id: str) -> None:
        self.collection.delete_one({'id': doc_id})
        
    def clear(self) -> None:
        self.collection.delete_many({})
    
    def search(self, query_vector: list[float], top_k: int) -> list[dict]:
        pipeline = [
            {
                '$vectorSearch': {
                    'index': 'vector_index',
                    'path': 'vector',
                    'queryVector': query_vector,
                    'numCandidates': 100,
                    'limit': top_k
                }
            },
            {
                '$project': {
                    {'_id': 0}
                }
            }
        ]
        
        return list(self.collection.aggregate(pipeline))
    
    def close(self) -> None:
        self.client.close()