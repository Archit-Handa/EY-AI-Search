import inspect
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
    chunker = _chunkers.get(chunker_type.lower())
    
    if chunker is None:
        raise ValueError(f'Unknown chunker type: {chunker_type}')
    
    return chunker(**kwargs) if inspect.signature(chunker).parameters else chunker()


__all__ = ['get_chunker']