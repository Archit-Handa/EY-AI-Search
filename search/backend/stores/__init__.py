from .base import Store
from .vector_store import VectorStore
from .text_store import TextStore

_STORES = {
    'vector': VectorStore,
    'text': TextStore
}

def get_store(store_type: str) -> Store:
    '''
    Retrieve the store for storing data
    
    @param store_type: Type of store
    @return: Store for storing data
    '''
    store_class = _STORES.get(store_type.lower())
    if store_class is None:
        raise ValueError(f'Unknown store type: {store_type}')
    
    return store_class()

    
__all__ = ['get_store']