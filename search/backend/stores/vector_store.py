from .base import Store
from dotenv import load_dotenv
import pymongo
import os

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
            print('⚠️ No existing embeddings found in collection. Index creation deferred until documents are added.')
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
                    'cosmosSearchOptions': cosmos_search_options.get(index_type.lower(), cosmos_search_options['ivf'])
                }
            ]
        }
        
        try:
            self.db.command(index_definition)
            print(f'✅ Created {index_type} Vector Index with {num_dimensions} dimensions')
        except Exception as e:
            print(f'❌ Error creating vector index: {e}')

    def add(self, documents: list[dict]) -> None:
        if not documents:
            print('⚠️ No documents provided for insertion.')
            return
        try:
            self.collection.insert_many(documents)
            print(f'✅ Successfully inserted {len(documents)} documents into vector store.')
            
            self._ensure_index()
            
        except Exception as e:
            print(f'❌ Bulk insert failed: {e}\nRetrying individually...')
            
            for doc in documents:
                try:
                    self.collection.insert_one(doc)
                except Exception as err:
                    print(f'❌ Failed to insert document {doc.get('id')}: {err}')
    
    def get(self, doc_id: str) -> dict:
        return self.collection.find_one({'id': doc_id}, {'_id': 0})
    
    def delete(self, doc_id: str) -> None:
        self.collection.delete_one({'id': doc_id})
        
    def clear(self) -> None:
        self.collection.delete_many({})
        self.collection.drop_indexes()
    
    def search(self, query_vector: list[float], top_k: int=5) -> list[dict]:
        if not query_vector:
            print('⚠️ No query vector provided for search.')
            return []
        
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
        
        try:
            return list(self.collection.aggregate(pipeline))
        
        except Exception as e:
            print(f'❌ Search failed: {e}')
            return []
    
    def close(self) -> None:
        self.client.close()