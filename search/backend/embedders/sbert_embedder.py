from .base import Embedder
from sentence_transformers import SentenceTransformer

class SBertEmbedder(Embedder):
    def __init__(self, model_name: str='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def _embed(self, input: list[str]) -> list[list[float]]:
        try:
            return self.model.encode(input, normalize_embeddings=True)
        
        except Exception as e:
            print(f'Error embedding text: {e}')
            return []