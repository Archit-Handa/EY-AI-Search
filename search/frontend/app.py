import streamlit as st
from document_fetchers import get_fetcher
from extract_file import extract_file
from chunk_text import chunk_text

def main():
    st.set_page_config('AI Search - EY')
    st.title('AI Search - EY')
    
    fetch_option = st.radio(
        label='Choose how to upload file:',
        options=[
            'Upload a file',
            'Fetch from Azure'
        ]
    )
    
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = None
    if 'chunks' not in st.session_state:
        st.session_state.chunks = None
    if 'loading' not in st.session_state:
        st.session_state.loading = False
    if 'error' not in st.session_state:
        st.session_state.error = None
        
    fetched = fetch_option == 'Fetch from Azure'
    
    fetcher = get_fetcher('azure' if fetched else 'upload')
    file = fetcher.fetch_document()
    
    if file is not None:
        col1, col2 = st.columns([0.5, 0.5])
        
        with col1:
            if st.button(
                label='Extract Text',
                disabled=st.session_state.loading,
                icon='📤'
            ):
                st.session_state.loading = True
                st.session_state.error = None
                
                with st.spinner('Extracting Text...'):
                    st.toast('Extracting Text...', icon='⌛')
                    try:
                        extracted_text = extract_file(file, fetched)
                        if extracted_text:
                            st.session_state.extracted_text = extracted_text
                            st.toast('Text Extracted Successfully', icon='✅')
                        else:
                            raise ValueError('No text could be extracted')
                    
                    except Exception as e:
                        st.session_state.error = str(e)
                        st.toast('Extraction Failed', icon='❌')
                    
                    finally:
                        st.session_state.loading = False
                    
        with col2:
            if st.session_state.extracted_text and not st.session_state.error:
                # st.success('✅ Text Extracted')
                pass
            
            elif st.session_state.error:
                st.error(f'❌ {st.session_state.error}')
    
    if st.session_state.extracted_text:
        with st.expander('**Extracted Text**', expanded=False):
            with st.container(height=300):
                st.write(f'{st.session_state.extracted_text}')
        
        chunker_type = st.selectbox(
            label='Select Chunker Type',
            options=[
                'Page',
                'Paragraph',
                'Fixed Size'
            ]
        )
        col1, col2 = st.columns([0.5, 0.5])
        
        with col1:
            if st.button('Chunk Text', icon='✂️'):
                st.session_state.loading = True
                st.session_state.error = None
                with st.spinner('Chunking Text...'):
                    try:
                        chunks = chunk_text(st.session_state.extracted_text, chunker_type)
                        if chunks:
                            st.session_state.chunks = chunks
                            st.toast('Text Chunked Successfully', icon='✅')
                        else:
                            raise ValueError('No chunks were generated')
                    
                    except Exception as e:
                        st.session_state.error = str(e)
                        st.toast('Extraction Failed', icon='❌')
                    
                    finally:
                        st.session_state.loading = False
        
        with col2:
            if st.session_state.chunks and not st.session_state.error:
                # st.success('✅ Text Chunked')
                pass
            
            elif st.session_state.error:
                st.error(f'❌ {st.session_state.error}')
        
        if st.session_state.chunks:
            with st.expander('**Chunks**', expanded=False):
                with st.container(height=300):
                    for i, chunk in enumerate(st.session_state.chunks):
                        with st.chat_message('Chunks', avatar='✂️'):
                            st.write(f'**Chunk {i+1}:** {chunk}')


if __name__ == '__main__':
    main()