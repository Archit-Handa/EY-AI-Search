from .base import DocumentLoader
from .pdf_loader import PDFLoader
from .docx_loader import DocxLoader
from .txt_loader import TxtLoader
from .json_loader import JsonLoader

_loaders = {
    'pdf': PDFLoader(),
    'docx': DocxLoader(),
    'txt': TxtLoader(),
    'json': JsonLoader()
}

def get_loader(file_extension: str) -> DocumentLoader:
    try:
        return _loaders[file_extension.lower()]
    
    except KeyError:
        raise ValueError(f'Unknown file extension: {file_extension}')

__all__ = ['get_loader']