import streamlit as st
from document_fetchers import get_fetcher
from extract_file import extract_file
from chunk_text import chunk_text
from generate_embeddings import generate_chunk_embeddings
from query import query

def _set_session_state(reset=False):
    session_state_vars = [
        'extracted_text',
        'title',
        'chunks',
        'embedder_name',
        'model_name',
        'embeddings',
        'loading',
        'error',
        'query',
        'top_k',
        'results'
    ]
    
    if reset:
        for var in session_state_vars:
            if var in st.session_state:
                del st.session_state[var]
    
    for var in session_state_vars:
        if var not in st.session_state:
            st.session_state[var] = None if var != 'loading' else False

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
    
    _set_session_state()
        
    fetched = fetch_option == 'Fetch from Azure'
    
    fetcher = get_fetcher('azure' if fetched else 'upload')
    file = fetcher.fetch_document()
    
    if file is not None:
        st.session_state.title = file.name.split('/')[-1]
        
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
            
            st.session_state.embedder_name = st.selectbox(
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
            
            if st.session_state.embedder_name in model_dict:
                model_choice = st.selectbox(
                    label='Select Model',
                    options=model_dict[st.session_state.embedder_name]
                )
            
                st.session_state.model_name = st.text_input(
                    label='Enter Model Name:',
                    placeholder='e.g. my-model-name'
                ) if model_choice == 'Other Model' else model_choice
            
            else:
                st.session_state.model_name = None
                
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
                            embeddings = generate_chunk_embeddings(
                                chunks=st.session_state.chunks,
                                title=st.session_state.title,
                                embedder=st.session_state.embedder_name,
                                model=st.session_state.model_name
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
                    if len(st.session_state.embeddings) > 5: st.markdown('...')
                    
                st.subheader("Step 4: Semantic Search")
                st.session_state.query = st.text_input("Enter your search query:")
                st.session_state.top_k = st.slider("Number of results", 1, 10, 3)

                col1, col2 = st.columns([0.5, 0.5])
                
                with col1:
                    if st.button(
                        label='Search Query',
                        disabled=st.session_state.loading,
                        icon='🔍'
                    ):
                        st.toast('Searching Query...', icon='⌛')
                        st.session_state.loading = True
                        st.session_state.error = None
                        
                        with st.spinner('Searching Query...'):
                            try:
                                results = query(
                                    query=st.session_state.query,
                                    embedder_name=st.session_state.embedder_name,
                                    model_name=st.session_state.model_name,
                                    k=st.session_state.top_k
                                )
                                if results:
                                    st.session_state.results = results
                                    st.toast('Searched Query Successfully', icon='✅')
                                else:
                                    raise ValueError('No results were generated')
                            
                            except Exception as e:
                                st.session_state.error = str(e)
                                st.toast('Embedding Failed', icon='❌')
                            
                            finally:
                                st.session_state.loading = False
                
                with col2:
                    if st.session_state.results and not st.session_state.error:
                        # st.success('✅ Chunks Embedded')
                        pass
                    
                    elif st.session_state.error:
                        st.error(f'❌ {st.session_state.error}')
                        
                if st.session_state.results:
                    with st.expander('**Search Results**', expanded=True):
                        with st.container(height=600):
                            for i, result in enumerate(st.session_state.results):
                                with st.chat_message('Search Results', avatar='🔍'):
                                    st.write(f'##### :primary[Search Result {i+1}]')
                                    st.write(result['content'])
                                    st.write(f'**:primary[Title:]** {result["title"]}')
                                    st.write(f'**:primary[Score:]** {result["score"]:.4f}')
                                    if i < len(st.session_state.results) - 1: st.write('---') 


if __name__ == '__main__':
    main()