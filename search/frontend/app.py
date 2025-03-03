import streamlit as st
from document_fetchers import get_fetcher
from extract_file import extract_file

def main():
    st.set_page_config('AI Search - EY')
    st.title('AI Search - EY')
    
    option = st.radio('Choose how to upload file:', ('Upload a file', 'Fetch from Azure'))
    
    fetched = True
    if option == 'Upload a file':
        fetcher = get_fetcher('upload')
        fetched = False
    elif option == 'Fetch from Azure':
        fetcher = get_fetcher('azure')
    
    file = fetcher.fetch_document()
    
    if file is not None: extract_file(file, fetched)

if __name__ == '__main__':
    main()