from .base import Embedder
from .openai_embedder import OpenAIEmbedder
from .sbert_embedder import SBertEmbedder

def get_embedder(embedder_name: str, **kwargs) -> Embedder:
    if embedder_name.lower() == 'openai':
        return OpenAIEmbedder(**kwargs)
    
    elif embedder_name.lower() == 'sbert':
        return SBertEmbedder(**kwargs)
    
    else:
        raise ValueError(f'Unknown embedder: {embedder_name}')
    
__all__ = ['get_embedder']