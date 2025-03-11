from .base import DocumentFetcher
from .azure_document_fetcher import AzureDocumentFetcher
from .document_uploader import DocumentUploader
from typing import Union

_fetchers = {
    'azure': AzureDocumentFetcher(),
    'upload': DocumentUploader()
}

def get_fetcher(fetcher_type: str) -> DocumentFetcher:
    try:
        return _fetchers[fetcher_type.lower()]
    
    except KeyError:
        raise ValueError(f'Unknown document fetcher type: {type}')
    
__all__ = ['get_fetcher']