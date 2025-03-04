import streamlit as st
import requests

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

def extract_file(file, fetched=False):
    try:
        files = {'file': (file.name, file.getvalue())} if not fetched \
            else {'file': (file[0], file[1])}
        response = requests.post(f'{BACKEND_URL_PATH}/extract-text', files=files)
        
        if response.status_code == 200:
            return response.json().get('extracted_text', '').strip()
            
        else:
            raise ValueError(response.json().get('error', 'Text extraction failed'))
    
    except Exception as e:
        raise RuntimeError(f'Error in text extraction: {e}')