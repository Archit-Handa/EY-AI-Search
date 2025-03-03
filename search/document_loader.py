from abc import ABC, abstractmethod

class DocumentLoader(ABC):
    @abstractmethod
    def load(self, document):
        pass

class PDFLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        import fitz
        
        text = ''
        try:
            with fitz.open(stream=file_path.read(), filetype='pdf') as doc:
                for page in doc:
                    text += page.get_text('text') + '\n'
        except Exception as e:
            text = f'Error loading PDF: {e}'
        
        return text

# TODO: Add Docx Loader load() code
class DocxLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        ...
        
class TextLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
        
class JsonLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        import json
        
        print(file_path)
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
        
def get_loader(file_extension: str) -> DocumentLoader:
    loaders = {
        'pdf': PDFLoader(),
        'docx': DocxLoader(),
        'txt': TextLoader(),
        'json': JsonLoader()
    }
    
    return loaders.get(file_extension.lower(), None)