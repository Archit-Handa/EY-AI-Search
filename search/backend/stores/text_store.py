from .base import Store

class TextStore(Store):
    def __init__(self):
        pass
    
    def add(self, documents: list[dict]) -> None:
        pass
    
    def get(self, doc_id: str) -> dict:
        pass
    
    def delete(self, doc_id: str) -> None:
        pass
    
    def clear(self) -> None:
        pass
    
    def search(self, query_vector: list[float], top_k: int) -> list[dict]:
        pass
    
    def close(self) -> None:
        pass