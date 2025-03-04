import streamlit as st
from document_fetchers import get_fetcher
from extract_file import extract_file
from chunk_text import chunk_text

def main():
    st.set_page_config('AI Search - EY')
    st.title('AI Search - EY')
    
    option = st.radio('Choose how to upload file:', ('Upload a file', 'Fetch from Azure'))
    
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = None
    if 'chunks' not in st.session_state:
        st.session_state.chunks = None
        
    fetched = option == 'Fetch from Azure'
    fetcher = get_fetcher("azure" if fetched else "upload")
    file = fetcher.fetch_document()
    
    if file is not None and st.session_state.extracted_text is None:
        st.session_state.extracted_text = extract_file(file, fetched)
    
    if st.session_state.extracted_text and st.session_state.chunks is None:
        chunk_text(st.session_state.extracted_text)

if __name__ == '__main__':
    main()