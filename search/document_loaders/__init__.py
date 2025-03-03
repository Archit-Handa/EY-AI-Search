from .base import DocumentLoader
from .pdf_loader import PDFLoader
from .docx_loader import DocxLoader
from .txt_loader import TextLoader
from .json_loader import JsonLoader

def get_loader(file_extension: str) -> DocumentLoader:
    loaders = {
        'pdf': PDFLoader(),
        'docx': DocxLoader(),
        'txt': TextLoader(),
        'json': JsonLoader()
    }
    
    return loaders.get(file_extension.lower(), None)

__all__ = ['PDFLoader', 'DocxLoader', 'TextLoader', 'JsonLoader', 'get_loader']