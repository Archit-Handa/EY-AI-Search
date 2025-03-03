from .base import DocumentLoader
from .pdf_loader import PDFLoader
from .docx_loader import DocxLoader
from .txt_loader import TxtLoader
from .json_loader import JsonLoader

def get_loader(file_extension: str) -> DocumentLoader:
    '''
    Returns the appropriate document loader based on the file extension
    
    @param file_extension: The file extension of the document
    @return: The document loader
    '''
    loaders = {
        'pdf': PDFLoader(),
        'docx': DocxLoader(),
        'txt': TxtLoader(),
        'json': JsonLoader()
    }
    
    return loaders.get(file_extension.lower(), None)

__all__ = ['get_loader']