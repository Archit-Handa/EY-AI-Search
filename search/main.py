from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf_loader import PDFLoader

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    pdf_file = request.files['file']
    extracted_text = PDFLoader.load_pdf(pdf_file)
    
    return jsonify({'extracted_text': extracted_text}), 200

if __name__ == '__main__':
    app.run(debug=True)