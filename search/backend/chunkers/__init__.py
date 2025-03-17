import inspect
from .base import Chunker
from .page_chunker import PageChunker
from .paragraph_chunker import ParagraphChunker
from .sentence_chunker import SentenceChunker
from .fixed_size_chunker import FixedSizeChunker

_CHUNKERS = {
    'page': PageChunker,
    'paragraph': ParagraphChunker,
    'sentence': SentenceChunker,
    'fixed_size': FixedSizeChunker
}

def get_chunker(chunker_type: str, **kwargs) -> Chunker:
    '''
    Retrieve the appropriate chunker for the given chunker type
    
    @param chunker_type: Type of chunker to retrieve
    @return: Chunker to be used for chunking text
    '''
    chunker_class = _CHUNKERS.get(chunker_type.lower())
    
    if chunker_class is None:
        raise ValueError(f'Unknown chunker type: {chunker_type}')
    
    return chunker_class(**kwargs) if inspect.signature(chunker_class).parameters else chunker_class()


__all__ = ['get_chunker']