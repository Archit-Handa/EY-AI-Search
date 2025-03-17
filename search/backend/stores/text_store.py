from .base import Store
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import os

load_dotenv()

class TextStore(Store):
    def __init__(self):
        self.client = Elasticsearch(
            os.getenv('ELASTICSEARCH_HOST'),
            api_key=os.getenv('ELASTICSEARCH_API_KEY')
        )
        self.index_name = 'text_index'
    
        self._ensure_index()
    
    def _ensure_index(self) -> None:
        if self.client.indices.exists(index=self.index_name):
            return
        
        index_mapping = {
            'settings': {
                'analysis': {
                    'analyzer': {
                        'custom_analyzer': {
                            'type': 'custom',
                            'tokenizer': 'standard',
                            'filter': ['lowercase', 'stemmer'],
                            'stopwords': '_english_'
                        }
                    }
                }
            },
            'mappings': {
                'properties': {
                    'id': {'type': 'keyword'},
                    'title': {'type': 'text', 'analyzer': 'custom_analyzer'},
                    'content': {'type': 'text', 'analyzer': 'custom_analyzer'},
                    'metadata': {'type': 'object'}
                }
            }
        }
        
        
        try:
            self.client.indices.create(index=self.index_name, body=index_mapping)
            print(f'✅ Created Text Index')
        except Exception as e:
            print(f'❌ Error creating text index: {e}')
    
    def add(self, documents: list[dict]) -> None:
        if not documents:
            print('⚠️ No documents provided for insertion.')
            return
        
        for doc in documents:
            try:
                self.client.index(index=self.index_name, id=doc['id'], body=doc)
            
            except Exception as err:
                print(f'❌ Failed to insert document {doc.get("id")}: {err}')
        
        print(f'✅ Successfully inserted {len(documents)} documents into text store.')
    
    def get(self, doc_id: str) -> dict:
        try:
            return self.client.get(index=self.index_name, id=doc_id)['_source']
        except Exception:
            return {}
    
    def delete(self, doc_id: str) -> None:
        self.client.delete(index=self.index_name, id=doc_id, ignore=[404])
    
    def clear(self) -> None:
        self.client.indices.delete(index=self.index_name, ignore=[404])
    
    def search(self, query: str, top_k: int=5) -> list[dict]:
        if not query:
            print('⚠️ No query provided for search.')
            return []
        
        query_body = {
            'query': {
                'match': {
                    'content': {
                        'query': query,
                    }
                }
            },
            'size': top_k
        }
        
        try:
            results = self.client.search(index=self.index_name, body=query_body)
            return [{
                'score': hit['_score'],
                **hit['_source']
            } for hit in results['hits']['hits']]
        
        except Exception as e:
            print(f'❌ Search failed: {e}')
            return []
    
    def close(self) -> None:
        self.client.close()