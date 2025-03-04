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
    
    fetcher = get_fetcher('azure' if fetched else 'upload')
    file = fetcher.fetch_document()
    
    if file is not None:
        if st.button('Extract Text'):
            extracted_text = extract_file(file, fetched)
            if extracted_text:
                st.session_state.extracted_text = extracted_text
    
    if st.session_state.extracted_text:
        with st.expander('Extracted Text', expanded=False):
            st.text_area('Extracted Text:', st.session_state.extracted_text, height=300)
        
        chunker_type = st.selectbox('Select Chunker Type', ['Page', 'Paragraph', 'Fixed Size'])
        
        if st.button('Chunk Text'):
            st.session_state.chunks = chunk_text(st.session_state.extracted_text, chunker_type)
            
    if st.session_state.chunks:
        with st.expander('Chunks', expanded=False):
            st.text_area('Chunks:', '\n\n\n[SEP]\n\n\n'.join(st.session_state.chunks), height=300)


if __name__ == '__main__':
    main()