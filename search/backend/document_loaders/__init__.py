from .base import DocumentLoader
from .pdf_loader import PDFLoader
from .docx_loader import DocxLoader
from .txt_loader import TxtLoader
from .json_loader import JsonLoader

_LOADERS = {
    'pdf': PDFLoader,
    'docx': DocxLoader,
    'txt': TxtLoader,
    'json': JsonLoader
}

def get_loader(file_extension: str) -> DocumentLoader:
    '''
    Retrieve the loader for a given file extension
    
    @param file_extension: File extension of the document
    @return: Loader for the given file extension
    '''
    loader_class = _LOADERS.get(file_extension.lower())
    if loader_class is None:
        raise ValueError(f'Unknown file extension: {file_extension}')
        
    return loader_class()


__all__ = ['get_loader']