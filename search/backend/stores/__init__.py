from .base import Store
from .vector_store import VectorStore
from .text_store import TextStore

def get_store(store_type: str) -> Store:
    if store_type == 'vector':
        return VectorStore()
    elif store_type == 'text':
        return TextStore()
    else:
        raise ValueError(f'Unknown store type: {store_type}')
    
__all__ = ['get_store']