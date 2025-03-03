import streamlit as st
from .base import DocumentFetcher

class DocumentUploader(DocumentFetcher):
    def fetch_document(self):
        st.write('Upload a Document (PDF, DOCX, JSON, or TXT file)')
        return st.file_uploader('Upload your file', type=['pdf', 'docx', 'json', 'txt'])