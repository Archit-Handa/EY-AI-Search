from .base import DocumentLoader

# TODO: Add Docx Loader load() code
class DocxLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        ...