import fitz
from .base import DocumentLoader
from typing import BinaryIO

class PDFLoader(DocumentLoader):
    '''Loader for .pdf files'''
    
    def load(self, file_stream: BinaryIO) -> str:
        '''Extract text from a .pdf file stream'''
        try:
            with fitz.open(stream=file_stream.read(), filetype='pdf') as doc:
                return '\n'.join(page.get_text('text').strip() for page in doc)
        except Exception as e:
            raise ValueError(f'Error extracting text from PDF: {e}')