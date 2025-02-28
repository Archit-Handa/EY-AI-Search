import fitz  # PyMuPDF
from flask import Flask, request, jsonify
import streamlit as st
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='https://ey-ai-search.streamlit.app/')

def load_pdf(pdf_file):
    """
    Load and extract text from a PDF file using PyMuPDF.
    :param pdf_file: Uploaded PDF file object
    :return: Extracted text as a string
    """
    text = ""
    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        text = f"Error loading PDF: {e}"
    
    return text

@app.route("/extract-text", methods=["POST"])
def extract_text():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    print(request.files)
    
    pdf_file = request.files["file"]
    extracted_text = load_pdf(pdf_file)
    
    return jsonify({"extracted_text": extracted_text})

if __name__ == "__main__":
    app.run(debug=True)