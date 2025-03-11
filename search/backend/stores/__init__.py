from .base import Store
from .vector_store import VectorStore
from .text_store import TextStore

_stores = {
    'vector': VectorStore(),
    'text': TextStore()
}

def get_store(store_type: str) -> Store:
    try:
        return _stores[store_type.lower()]
    
    except KeyError:
        raise ValueError(f'Unknown store type: {store_type}')
    
__all__ = ['get_store']