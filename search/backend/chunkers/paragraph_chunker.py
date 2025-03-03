from .base import Chunker

class ParagraphChunker(Chunker):
    '''Chunk a text into smaller chunks based on paragraph breaks'''
    
    # TODO: Implement paragraph chunker
    def chunk(self, text: str) -> list[str]:
        ...