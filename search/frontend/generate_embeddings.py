import streamlit as st
import requests

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

def generate_embeddings(input, embedder, model):
    try:
        request_body = {
            'input': input,
            'embedder': embedder
        }
        
        if model:
            request_body['model'] = model
            
        response = requests.post(f'{BACKEND_URL_PATH}/embed-text', json=request_body)
        
        if response.status_code == 200:
            return response.json().get('embeddings', [])
            
        else:
            raise ValueError(response.json().get('error', 'Text embedding failed'))
    
    except Exception as e:
        raise RuntimeError(f'Error in embedding: {e}')
    