import streamlit as st
import requests

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

def generate_chunk_embeddings(chunks, title, embedder, model):
    try:
        request_body = {
            'chunks': chunks,
            'title': title,
            'embedder': embedder
        }
        
        if model:
            request_body['model'] = model
            
        response = requests.post(f'{BACKEND_URL_PATH}/embed-chunks', json=request_body)
        
        if response.status_code == 200:
            return response.json().get('embeddings', [])
            
        else:
            raise ValueError(response.json().get('error', 'Text embedding failed'))
    
    except Exception as e:
        raise RuntimeError(f'Error in embedding: {e}')
    