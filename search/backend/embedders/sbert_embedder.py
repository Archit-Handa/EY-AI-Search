from .base import Embedder
from sentence_transformers import SentenceTransformer

class SBertEmbedder(Embedder):
    def __init__(self, model_name: str='all-MiniLM-L6-v2'):
        try:
            self.model = SentenceTransformer(model_name)
        
        except Exception as e:
            raise RuntimeError(f'Error loading SBert model: {e}')
    
    def _embed(self, input: list[str]) -> list[list[float]]:
        try:
            return self.model.encode(input, normalize_embeddings=True).tolist()
        
        except Exception as e:
            raise RuntimeError(f'Error embedding text with SBert: {e}')