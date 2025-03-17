from .base import Embedder
from .openai_embedder import OpenAIEmbedder
from .sbert_embedder import SBertEmbedder

_EMBEDDERS = {
    'openai': OpenAIEmbedder,
    'sbert': SBertEmbedder
}

def get_embedder(embedder_type: str, **kwargs) -> Embedder:
    embedder_class = _EMBEDDERS.get(embedder_type.lower())
    if embedder_class is None:
        raise ValueError(f'Unknown embedder: {embedder_type}')
    
    return embedder_class(**kwargs)
    
__all__ = ['get_embedder']