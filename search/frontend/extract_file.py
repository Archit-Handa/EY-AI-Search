import streamlit as st
import requests

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

def extract_file(file, fetched=False):
    with st.status('Extracting Text...', expanded=True) as status:
        files = {'file': (file.name, file.getvalue())} if not fetched \
            else {'file': (file[0], file[1])}
        response = requests.post(f'{BACKEND_URL_PATH}/extract-text', files=files)
        
        if response.status_code == 200:
            status.update(label='Text Extracted', state='complete')
            return response.json().get('extracted_text', 'No text extracted')
            
        else:
            status.update(label='Failed to extract text', state='error')
            st.error('Failed to extract text.')
            return None