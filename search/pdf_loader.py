import fitz

class PDFLoader:
    def __init__(self):
        pass
    
    @staticmethod
    def load_pdf(pdf_file):
        text = ''
        try:
            with fitz.open(stream=pdf_file.read(), filetype='pdf') as doc:
                for page in doc:
                    text += page.get_text('text') + '\n'
        except Exception as e:
            text = f'Error loading PDF: {e}'
        
        return text