import streamlit as st

def main():
    st.title('AI Search - EY')
    st.write('Upload a Document (PDF, DOCX, JSON, or TXT file)')
    
    uploaded_file = st.file_uploader('Upload your file', type=['pdf', 'docx', 'json', 'txt'])
    
    if uploaded_file is not None:
        st.write(f'### Uploaded File: {uploaded_file.name}')

if __name__ == '__main__':
    main()