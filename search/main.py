from flask import Flask, request, jsonify
from flask_cors import CORS
from document_loader import get_loader

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    doc_loader = get_loader(file.filename.split('.')[-1])
    
    if doc_loader is None:
        return jsonify({'error': 'Unsupported file format'}), 400
    
    extracted_text = doc_loader.load(file)
    
    return jsonify({'extracted_text': extracted_text}), 200

if __name__ == '__main__':
    app.run(debug=True)