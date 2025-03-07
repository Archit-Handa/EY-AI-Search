from flask import Flask, request, jsonify
from flask_cors import CORS
from document_loaders import get_loader
from chunkers import get_chunker
from embedders import get_embedder
from stores import get_store

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
    chunk_size = request.json.get('chunk_size', 200)
    chunker = get_chunker(chunker_type, **{'chunk_size': chunk_size})
    
    if chunker is None:
        return jsonify({'error': 'Unsupported chunker type'}), 400
    
    chunks = chunker.chunk(text)
    
    return jsonify({'chunks': list(chunks)}), 200

@app.post('/embed-text')
def embed_text():
    if 'input' not in request.json:
        return jsonify({'error': 'No text provided'}), 400
    
    if 'embedder' not in request.json:
        return jsonify({'error': 'No embedder type provided'}), 400
    
    input = request.json['input']
    embedder_type = request.json['embedder']
    model_name = request.json.get('model')
    embedder = get_embedder(embedder_type, **{'model_name': model_name} if model_name else {})
    
    if embedder is None:
        return jsonify({'error': 'Unsupported embedder type'}), 400
    
    embeddings = embedder(input)
    
    return jsonify({'embeddings': embeddings}), 200

@app.post('/store-embeddings')
def store_embeddings():
    if 'embeddings' not in request.json:
        return jsonify({'error': 'No embeddings provided'}), 400
    
    if 'contents' not in request.json:
        return jsonify({'error': 'No contents provided'}), 400
    
    embeddings = request.json['embeddings']
    contents = request.json['contents']
    title = request.json.get('title', 'Untitled')
    
    vector_store = get_store('vector')
    vector_store.add([
        {
            'content': content,
            'vector': embedding,
            'title': title
        } for embedding, content in zip(embeddings, contents)
    ])
    
    return jsonify({'message': 'Successfully stored embeddings'}), 200

if __name__ == '__main__':
    app.run(debug=True)