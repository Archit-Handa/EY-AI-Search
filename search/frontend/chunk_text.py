import streamlit as st
import requests

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

def chunk_text(text, chunker_type='page', **kwargs):
    try:
        request_body = {
            'text': text,
            'type': chunker_type.replace(' ', '_').lower(),
            **kwargs
        }
        response = requests.post(f'{BACKEND_URL_PATH}/chunk-text', json=request_body)
        
        if response.status_code == 200:
            return response.json().get('chunks', [])
            
        else:
            raise ValueError(response.json().get('error', 'Text chunking failed'))
    
    except Exception as e:
        raise RuntimeError(f'Error in chunking: {e}')