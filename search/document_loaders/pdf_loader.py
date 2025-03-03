import fitz
from .base import DocumentLoader

class PDFLoader(DocumentLoader):
    def load(self, file_stream: str) -> str:
        text = ''
        try:
            with fitz.open(stream=file_stream.read(), filetype='pdf') as doc:
                for page in doc:
                    text += page.get_text('text') + '\n'
        except Exception as e:
            text = f'Error loading PDF: {e}'
        
        return text