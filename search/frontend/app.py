import streamlit as st
from document_fetchers import get_fetcher
from extract_file import extract_file
from chunk_text import chunk_text
from generate_embeddings import generate_embeddings

def _set_session_state(reset=False):
    if reset:
        st.session_state.extracted_text = None
        st.session_state.chunks = None
        st.session_state.embeddings = None
        st.session_state.loading = False
        st.session_state.error = None
    
    else:
        if 'extracted_text' not in st.session_state:
            st.session_state.extracted_text = None
        if 'chunks' not in st.session_state:
            st.session_state.chunks = None
        if 'embeddings' not in st.session_state:
            st.session_state.embeddings = None
        if 'loading' not in st.session_state:
            st.session_state.loading = False
        if 'error' not in st.session_state:
            st.session_state.error = None

def main():
    st.set_page_config('AI Search - EY')
    st.title('AI Search - EY')
    
    st.subheader('Step 1: Load document and extract text')
    
    fetch_option = st.radio(
        label='Choose how to upload file:',
        options=[
            'Upload a file',
            'Fetch from Azure'
        ]
    )
    
    # if 'extracted_text' not in st.session_state:
    #     st.session_state.extracted_text = None
    # if 'chunks' not in st.session_state:
    #     st.session_state.chunks = None
    # if 'embeddings' not in st.session_state:
    #     st.session_state.embeddings = None
    # if 'loading' not in st.session_state:
    #     st.session_state.loading = False
    # if 'error' not in st.session_state:
    #     st.session_state.error = None
    _set_session_state()
        
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
                st.toast('Extracting Text...', icon='⌛')
                st.session_state.loading = True
                st.session_state.error = None
                
                with st.spinner('Extracting Text...'):
                    try:
                        extracted_text = extract_file(
                            file=file,
                            fetched=fetched
                        )
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
                st.text(f'{st.session_state.extracted_text}')
        
        st.subheader('Step 2: Split text into chunks')
        
        chunker_type = st.selectbox(
            label='Select Chunker Type',
            options=[
                'Page',
                'Paragraph',
                'Sentence',
                'Fixed Size'
            ]
        )
        
        chunk_size = None
        if chunker_type == 'Fixed Size':
            chunk_size = st.number_input(
                label='Enter chunk size (in characters)',
                min_value=50,
                max_value=2000,
                value=500,
                step=50
            )
        
        col1, col2 = st.columns([0.5, 0.5])
        
        with col1:
            if st.button(
                label='Chunk Text',
                disabled=st.session_state.loading,
                icon='✂️'
            ):
                st.toast('Chunking Text...', icon='⌛')
                st.session_state.loading = True
                st.session_state.error = None
                
                with st.spinner('Chunking Text...'):
                    try:
                        chunks = chunk_text(
                            text=st.session_state.extracted_text,
                            chunker_type=chunker_type,
                            **{'chunk_size': chunk_size}
                        )
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
                            
            st.subheader('Step 3: Generate chunk embeddings')
            
            embedder_name = st.selectbox(
                label='Select Embedder',
                options=[
                    'SBert',
                    'OpenAI'
                ]
            )
            
            model_dict = {
                'SBert': [
                    'all-MiniLM-L6-v2',
                    'all-mpnet-base-v2',
                    'multi-qa-MiniLM-L6-cos-v1',
                    'Other Model'
                ],
                'OpenAI': [
                    'text-embedding-ada-002',
                    'text-embedding-3-small',
                    'text-embedding-3-large',
                    'Other Model'
                ]
            }
            
            if embedder_name in model_dict:
                model_choice = st.selectbox(
                    label='Select Model',
                    options=model_dict[embedder_name]
                )
            
                model_name = st.text_input(
                    label='Enter Model Name:',
                    placeholder='e.g. my-model-name'
                ) if model_choice == 'Other Model' else model_choice
            
            else:
                model_name = None
                
            col1, col2 = st.columns([0.5, 0.5])
            
            with col1:
                if st.button(
                    label='Generate Embeddings',
                    disabled=st.session_state.loading,
                    icon='🧠'
                ):
                    st.toast('Generating Embeddings...', icon='⌛')
                    st.session_state.loading = True
                    st.session_state.error = None
                    
                    with st.spinner('Generating Embeddings...'):
                        try:
                            embeddings = generate_embeddings(
                                input=st.session_state.chunks,
                                embedder=embedder_name,
                                model=model_name
                            )
                            if embeddings:
                                st.session_state.embeddings = embeddings
                                st.toast('Chunks Embedded Successfully', icon='✅')
                            else:
                                raise ValueError('No embeddings were generated')
                        
                        except Exception as e:
                            st.session_state.error = str(e)
                            st.toast('Embedding Failed', icon='❌')
                        
                        finally:
                            st.session_state.loading = False
            
            with col2:
                if st.session_state.chunks and not st.session_state.error:
                    # st.success('✅ Chunks Embedded')
                    pass
                
                elif st.session_state.error:
                    st.error(f'❌ {st.session_state.error}')
                    
            if st.session_state.embeddings:
                with st.expander('**Chunk Embeddings**', expanded=False):
                    for i, embedding in enumerate(st.session_state.embeddings[:5]):
                        formatted_embedding = f'**Embedding {i+1}:**&emsp;`[{", ".join(f"{x:+.4f}" for x in embedding[:5]).replace("+", " ")} ...]`'
                        st.markdown(formatted_embedding, unsafe_allow_html=True)
                    st.markdown('...')


if __name__ == '__main__':
    main()