import streamlit as st
from azure.storage.blob import BlobServiceClient
from io import BytesIO
from .base import DocumentFetcher

class AzureDocumentFetcher(DocumentFetcher):
    '''Fetch and return a document from Azure Blob Storage'''
    
    def fetch_document(self):
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
            
            if filename:
                blob_client = container_client.get_blob_client(filename)
                blob_stream = BytesIO(blob_client.download_blob().readall())
            
            return filename, blob_stream
        
        return None