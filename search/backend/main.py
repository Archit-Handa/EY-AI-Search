from flask import Flask, request, jsonify
from flask_cors import CORS
from document_loaders import get_loader
from chunkers import get_chunker

app = Flask(__name__)
CORS(app, origins='*')

@app.post('/extract-text')
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    doc_loader = get_loader(file.filename.split('.')[-1])
    
    if doc_loader is None:
        return jsonify({'error': 'Unsupported file format'}), 400
    
    extracted_text = doc_loader.load(file)
    
    return jsonify({'extracted_text': extracted_text}), 200

@app.post('/chunk-text')
def chunk_text():
    if 'text' not in request.json:
        return jsonify({'error': 'No text provided'}), 400
    
    if 'type' not in request.json:
        return jsonify({'error': 'No chunker type provided'}), 400
    
    text = request.json['text']
    chunker_type = request.json['type']
    chunker = get_chunker(chunker_type)
    
    if chunker is None:
        return jsonify({'error': 'Unsupported chunker type'}), 400
    
    chunks = chunker.chunk(text)
    
    return jsonify({'chunks': chunks}), 200

if __name__ == '__main__':
    app.run(debug=True)