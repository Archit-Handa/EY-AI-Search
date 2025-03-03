from .base import DocumentFetcher
from .azure_document_fetcher import AzureDocumentFetcher
from .document_uploader import DocumentUploader
from typing import Union

def get_fetcher(type: str) -> Union[DocumentFetcher, DocumentUploader]:
    if type == 'azure':
        return AzureDocumentFetcher()
    elif type == 'upload':
        return DocumentUploader()
    else:
        raise ValueError(f'Unknown document fetcher type: {type}')
    
__all__ = ['get_fetcher']