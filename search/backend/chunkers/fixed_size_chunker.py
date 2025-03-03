from .base import Chunker

class FixedSizeChunker(Chunker):
    '''Chunk a text into smaller chunks of a fixed size'''
    
    # TODO: Implement fixed size chunker
    def chunk(self, text: str) -> list[str]:
        ...