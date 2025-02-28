import streamlit as st
import requests

def main():
    st.title('AI Search - EY')
    st.write('Upload a Document (PDF, DOCX, JSON, or TXT file)')
    
    uploaded_file = st.file_uploader('Upload your file', type=['pdf', 'docx', 'json', 'txt'])
    
    if uploaded_file is not None:
        # st.write('Uploaded file:', uploaded_file.name)
        extract_button = st.empty()
        if extract_button.button('Extract Text'):
            with st.status('Extracting Text...', expanded=True) as status:
                files = {'file': uploaded_file.getvalue()}
                response = requests.post('http://127.0.0.1:5000/extract-text', files=files)
                
                if response.status_code == 200:
                    status.update(label='Text Extracted', state='complete')
                    extracted_text = response.json().get('extracted_text', 'No text extracted')
                    st.text_area('Extracted Text:', extracted_text, height=300)
                    extract_button.empty()
                    
                else:
                    status.update(label='Failed to extract text', state='error')
                    st.error('Failed to extract text.')

if __name__ == '__main__':
    main()