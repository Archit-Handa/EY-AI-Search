import docx
from io import BytesIO
from .base import DocumentLoader

class DocxLoader(DocumentLoader):
    '''Loader for .docx files'''
    
    def load(self, file_stream: str) -> str:
        doc = docx.Document(BytesIO(file_stream.read()))
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text.strip()