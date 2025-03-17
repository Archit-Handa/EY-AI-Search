from .base import Embedder
from .openai_embedder import OpenAIEmbedder
from .sbert_embedder import SBertEmbedder

_embedders = {
    'openai': OpenAIEmbedder,
    'sbert': SBertEmbedder
}

def get_embedder(embedder_type: str, **kwargs) -> Embedder:
    try:
        return _embedders[embedder_type.lower()](**kwargs)
    
    except KeyError:
        raise ValueError(f'Unknown embedder: {embedder_type}')
    
__all__ = ['get_embedder']