import docx
from io import BytesIO
from .base import DocumentLoader
from typing import BinaryIO

class DocxLoader(DocumentLoader):
    '''Loader for .docx files'''
    
    def load(self, file_stream: BinaryIO) -> str:
        '''Extract text from a .docx file stream'''
        doc = docx.Document(BytesIO(file_stream.read()))
        text = '\n'.join(map(str.strip, (para.text for para in doc.paragraphs)))
        return text.strip()