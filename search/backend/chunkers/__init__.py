from .base import Chunker
from .page_chunker import PageChunker
from .paragraph_chunker import ParagraphChunker
from .sentence_chunker import SentenceChunker
from .fixed_size_chunker import FixedSizeChunker

def get_chunker(type: str, **kwargs) -> Chunker:
    if type == 'page':
        return PageChunker()
    elif type == 'paragraph':
        return ParagraphChunker()
    elif type == 'sentence':
        return SentenceChunker()
    elif type == 'fixed_size':
        return FixedSizeChunker(**kwargs)
    else:
        raise ValueError(f'Unknown chunker type: {type}')

__all__ = ['get_chunker']