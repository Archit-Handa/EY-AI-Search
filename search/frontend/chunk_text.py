import streamlit as st
import requests

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

def chunk_text(text, chunker_type='page'):
    with st.status('Chunking Text...', expanded=True) as status:
        request_body = {'text': text, 'type': chunker_type.replace(' ', '_').lower()}
        response = requests.post(f'{BACKEND_URL_PATH}/chunk-text', json=request_body)
        
        if response.status_code == 200:
            status.update(label='Text Chunked', state='complete')
            return response.json().get('chunks', [])
            
        else:
            status.update(label='Failed to extract text', state='error')
            st.error('Failed to extract text.')
            return []