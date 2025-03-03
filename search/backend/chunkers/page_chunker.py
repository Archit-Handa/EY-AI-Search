from .base import Chunker

class PageChunker(Chunker):
    '''Chunk a text into smaller chunks based on page breaks'''
    
    # TODO: Implement page chunker
    def chunk(self, text: str) -> list[str]:
        ...