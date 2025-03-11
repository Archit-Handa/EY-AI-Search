from .base import Store
from dotenv import load_dotenv
import pymongo
import os
import uuid

load_dotenv()

class VectorStore(Store):
    '''Vector Store that uses CosmosDB (MongoDB for Azure) to store embeddings'''
    
    def __init__(self, index_type: str='IVF'):
        self.client = pymongo.MongoClient(os.getenv('COSMOSDB_CONNECTION_STRING'))
        self.db = self.client[os.getenv('COSMOSDB_DATABASE_NAME')]
        self.collection = self.db['embeddings']
    
        self._ensure_index(index_type=index_type)
        
    def _ensure_index(self, index_type: str='IVF') -> None:
        indexes = self.collection.index_information()
        
        if 'vector_index' in indexes:
            return
        
        sample_doc = self.collection.find_one({}, {'vector': 1})
        if sample_doc and 'vector' in sample_doc:
            num_dimensions = len(sample_doc['vector'])
        else:
            print('⚠️ No existing embeddings found in collection. Index creation deferred to post insertion of documents.')
            return
        
        cosmos_search_options = {
            'ivf': {
                'kind': 'vector-ivf',
                'numLists': 100,
                'similarity': 'COS',
                'dimensions': num_dimensions
            },
            
            # TESTME: HNSW and DiskANN Indexes have not been tested yet as they require cluster of tier M40 or higher
            'hnsw': {
                'kind': 'vector-hnsw',
                'm': 32,
                'efConstruction': 64,
                'similarity': 'COS',
                'dimensions': num_dimensions
            },
            'diskann': {
                'kind': 'vector-diskann',
                'maxDegree': 32,
                'lBuild': 50,
                'similarity': 'COS',
                'dimensions': num_dimensions
            }
        }
        
        index_definition = {
            'createIndexes': self.collection.name,
            'indexes': [
                {
                    'name': 'vector_index',
                    'key': {
                        'vector': 'cosmosSearch'
                    },
                    'cosmosSearchOptions': cosmos_search_options.get(index_type.lower(), cosmos_search_options.get('ivf'))
                }
            ]
        }
        
        try:
            self.db.command(index_definition)
            print(f'✅ Created {index_type} Index with {num_dimensions} dimensions')
        except Exception as e:
            print(f'❌ Error creating index: {e}')

    def add(self, documents: list[dict]) -> None:
        if not documents:
            return
        
        for doc in documents:
            doc['id'] = str(uuid.uuid4())
            doc.setdefault('metadata', {})
        
        self.collection.insert_many(documents)
        
        self._ensure_index()
    
    def get(self, doc_id: str) -> dict:
        return self.collection.find_one({'id': doc_id}, {'_id': 0})
    
    def delete(self, doc_id: str) -> None:
        self.collection.delete_one({'id': doc_id})
        
    def clear(self) -> None:
        self.collection.delete_many({})
        self.collection.drop_index('vector_index')
    
    def search(self, query_vector: list[float], top_k: int) -> list[dict]:
        pipeline = [
            {
                '$search': {
                    'cosmosSearch': {
                        'vector': query_vector,
                        'path': 'vector',
                        'k': top_k
                    },
                    'returnStoredSource': True
                }
            },
            {
                '$project': {
                    'similarityScore': {
                        '$meta': 'searchScore'
                    },
                    'document' : '$$ROOT'
                }
            }
        ]
            
        return list(self.collection.aggregate(pipeline))
    
    def close(self) -> None:
        self.client.close()