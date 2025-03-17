from .base import DocumentFetcher
from .azure_document_fetcher import AzureDocumentFetcher
from .document_uploader import DocumentUploader
from typing import Union

_FETCHERS = {
    'azure': AzureDocumentFetcher,
    'upload': DocumentUploader
}

def get_fetcher(fetcher_type: str) -> DocumentFetcher:
    fetcher_class = _FETCHERS.get(fetcher_type.lower())
    if fetcher_class is None:
        raise ValueError(f'Unknown document fetcher type: {fetcher_type}')
    
    return fetcher_class()
    
__all__ = ['get_fetcher']