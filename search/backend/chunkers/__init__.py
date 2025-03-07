from .base import Chunker
from .page_chunker import PageChunker
from .paragraph_chunker import ParagraphChunker
from .sentence_chunker import SentenceChunker
from .fixed_size_chunker import FixedSizeChunker

_chunkers = {
    'page': PageChunker,
    'paragraph': ParagraphChunker,
    'sentence': SentenceChunker,
    'fixed_size': FixedSizeChunker
}

def get_chunker(chunker_type: str, **kwargs) -> Chunker:
    try:
        return _chunkers[chunker_type.lower()](**kwargs)
    
    except KeyError:
        raise ValueError(f'Unknown chunker type: {type}')

__all__ = ['get_chunker']