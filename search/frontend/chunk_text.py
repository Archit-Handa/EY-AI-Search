import streamlit as st
import requests

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

def chunk_text(text):
    chunker_type = st.selectbox('Select Chunker Type', ['Page', 'Paragraph', 'Fixed Size'])
    chunk_button = st.empty()
    print('before clicking chunk button')
    if chunk_button.button('Chunk Text'):
        print('chunk button clicked')
        with st.status('Chunking Text...', expanded=True) as status:
            request_body = {'text': text, 'type': chunker_type.replace(' ', '_').lower()}
            response = requests.post(f'{BACKEND_URL_PATH}/chunk-text', json=request_body)
            print('request sent')
            if response.status_code == 200:
                status.update(label='Text Chunked', state='complete')
                chunks = response.json().get('chunks', 'No text chunked')
                for chunk in chunks:
                    st.write(chunk + '\n\n\n<>\n\n\n')
                chunk_button.empty()
                
            else:
                status.update(label='Failed to extract text', state='error')
                st.error('Failed to extract text.')