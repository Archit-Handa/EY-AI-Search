import streamlit as st
import requests
from azure.storage.blob import BlobServiceClient
from io import BytesIO

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

def upload_file():
    st.write('Upload a Document (PDF, DOCX, JSON, or TXT file)')
    return st.file_uploader('Upload your file', type=['pdf', 'docx', 'json', 'txt'])

def fetch_azure_file():
    AZURE_CONNECTION_STRING = st.text_input(
        label='Azure Storage Connection String',
        value=None,
        placeholder='Enter your Azure storage connection string',
        type='password'
    )
    CONTAINER_NAME = st.text_input(
        label='Container Name',
        value=None,
        placeholder='Enter your container name'
    )
    
    if AZURE_CONNECTION_STRING is not None and CONTAINER_NAME is not None:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        blob_list = [blob.name for blob in container_client.list_blobs()]
        filename = st.selectbox("Choose a file from Azure Blob Storage:", blob_list)
        
        blob_client = container_client.get_blob_client(filename)
        blob_stream = BytesIO(blob_client.download_blob().readall())
        
        return filename, blob_stream
    
    return None

def extract_file(file, fetched=False):
    extract_button = st.empty()
    if extract_button.button('Extract Text'):
        with st.status('Extracting Text...', expanded=True) as status:
            files = {'file': (file.name, file.getvalue())} if not fetched \
                else {'file': (file[0], file[1])}
            response = requests.post(f'{BACKEND_URL_PATH}/extract-text', files=files)
            
            if response.status_code == 200:
                status.update(label='Text Extracted', state='complete')
                extracted_text = response.json().get('extracted_text', 'No text extracted')
                st.text_area('Extracted Text:', extracted_text, height=300)
                extract_button.empty()
                
            else:
                status.update(label='Failed to extract text', state='error')
                st.error('Failed to extract text.')

def main():
    st.set_page_config('AI Search - EY')
    st.title('AI Search - EY')
    
    option = st.radio('Choose how to upload file:', ('Upload a file', 'Fetch from Azure'))
            
    file, fetched = (upload_file(), False) if option == 'Upload a file' \
        else (fetch_azure_file(), True) if option == 'Fetch from Azure' \
            else (None, None)
            
    if file is not None: extract_file(file, fetched)

if __name__ == '__main__':
    main()