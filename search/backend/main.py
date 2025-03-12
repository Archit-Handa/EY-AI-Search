from flask import Flask, request, jsonify
from flask_cors import CORS
from document_loaders import get_loader
from chunkers import get_chunker
from embedders import get_embedder
from stores import get_store
import requests

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

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

@app.post('/embed-chunks')
def embed_chunks():
    if 'chunks' not in request.json:
        return jsonify({'error': 'No text provided'}), 400
    
    if 'title' not in request.json:
        return jsonify({'error': 'No title provided'}), 400
    
    if 'embedder' not in request.json:
        return jsonify({'error': 'No embedder type provided'}), 400
    
    chunks = request.json['chunks']
    title = request.json['title']
    embedder_type = request.json['embedder']
    model_name = request.json.get('model')
    embedder = get_embedder(embedder_type, **{'model_name': model_name} if model_name else {})
    
    if embedder is None:
        return jsonify({'error': 'Unsupported embedder type'}), 400
    
    embeddings = embedder(chunks)
    
    request_body = {
        'contents': chunks,
        'title': title,
        'embeddings': embeddings
    }
    response = requests.post(f'{BACKEND_URL_PATH}/store-embeddings', json=request_body)
    
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print(response.json()['error'])
        
    return jsonify({'embeddings': embeddings}), 200

@app.post('/store-embeddings')
def store_embeddings():
    if 'embeddings' not in request.json:
        return jsonify({'error': 'No embeddings provided'}), 400
    
    if 'contents' not in request.json:
        return jsonify({'error': 'No contents provided'}), 400
    
    embeddings = request.json['embeddings']
    contents = request.json['contents']
    title = request.json['title']
    
    vector_store = get_store('vector')
    vector_store.add([
        {
            'content': content,
            'vector': embedding,
            'title': title
        } for embedding, content in zip(embeddings, contents)
    ])
    
    text_store = get_store('text')
    text_store.add([
        {
            'content': content,
            'title': title
        } for content in contents
    ])
    
    return jsonify({'message': 'Successfully stored embeddings'}), 200

@app.post('/query')
def query():
    if 'query' not in request.json:
        return jsonify({'error': 'No query provided'}), 400
    
    if 'embedder' not in request.json:
        return jsonify({'error': 'No embedder type provided'}), 400
    
    if 'k' not in request.json:
        return jsonify({'error': 'No k value provided'}), 400
    
    query = request.json['query']
    embedder_type = request.json['embedder']
    model_name = request.json.get('model')
    top_k = request.json['k']
    
    semantic_search_request_body = {
        'query': query,
        'embedder': embedder_type,
        'model': model_name,
        'k': top_k
    }
    semantic_search_response = requests.post(f'{BACKEND_URL_PATH}/semantic-search', json=semantic_search_request_body)
    
    if semantic_search_response.status_code == 200:
        semantic_search_results = semantic_search_response.json()['results']
    else:
        return semantic_search_response.json()['error'], 400
    
    full_text_search_request_body = {
        'query': query,
        'k': top_k
    }
    full_text_search_response = requests.post(f'{BACKEND_URL_PATH}/full-text-search', json=full_text_search_request_body)
    
    if full_text_search_response.status_code == 200:
        full_text_search_results = full_text_search_response.json()['results']
    else:
        return full_text_search_response.json()['error'], 400
    
    # TODO: Integrate RRF API Endpoint
    
    # TODO: Integrate Cross-Encoder Reranking API Endpoint
    
    # FIXME: For now, just forwarding semantic and full-text search results
    return jsonify({'results': semantic_search_results + full_text_search_results}), 200

@app.post('/semantic-search')
def semantic_search():
    if 'query' not in request.json:
        return jsonify({'error': 'No query provided'}), 400
    
    if 'embedder' not in request.json:
        return jsonify({'error': 'No embedder type provided'}), 400
    
    if 'k' not in request.json:
        return jsonify({'error': 'No k value provided'}), 400
    
    query = request.json['query']
    embedder_type = request.json['embedder']
    model_name = request.json.get('model')
    top_k = request.json['k']
    
    embedder = get_embedder(embedder_type, **{'model_name': model_name} if model_name else {})
    
    if embedder is None:
        return jsonify({'error': 'Unsupported embedder type'}), 400
    
    query_vector = embedder(query)
    vector_store = get_store('vector')
    results = vector_store.search(query_vector, top_k=top_k)
    
    return jsonify({
        'results': [
            {
                'id': result['document']['id'],
                'title': result['document']['title'],
                'content': result['document']['content'],
                'metadata': result['document']['metadata'],
                # 'vector': result['document']['vector'],
                'score': result['similarityScore']
            } for result in results
        ]
    }), 200

@app.post('/full-text-search')
def full_text_search():
    if 'query' not in request.json:
        return jsonify({'error': 'No query provided'}), 400
    
    if 'k' not in request.json:
        return jsonify({'error': 'No k value provided'}), 400
    
    query = request.json['query']
    top_k = request.json['k']
    
    query = request.json['query']
    text_store = get_store('text')
    results = text_store.search(query, top_k=top_k)
    
    return jsonify({'results': results}), 200

@app.post('/rrf-results')
def rrf():
    pass

@app.post('/rerank-results')
def rerank():
    pass


if __name__ == '__main__':
    get_store('vector').clear()
    get_store('text').clear()
    app.run(debug=True)