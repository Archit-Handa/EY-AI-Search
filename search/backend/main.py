from flask import Flask, request, jsonify
from flask_cors import CORS
from document_loaders import get_loader
from chunkers import get_chunker
from embedders import get_embedder
from stores import get_store
import requests
import uuid
from collections import defaultdict

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
    ids = [str(uuid.uuid4()) for _ in embeddings]
    
    vector_store = get_store('vector')
    vector_store.add([
        {
            'id': _id,
            'metadata': {},
            'content': content,
            'vector': embedding,
            'title': title
        } for _id, embedding, content in zip(ids, embeddings, contents)
    ])
    
    text_store = get_store('text')
    text_store.add([
        {
            'id': _id,
            'metadata': {},
            'content': content,
            'title': title
        } for _id, content in zip(ids, contents)
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
        'k': top_k * 2      # Fetching more results than required; will filter while responding
    }
    semantic_search_response = requests.post(f'{BACKEND_URL_PATH}/semantic-search', json=semantic_search_request_body)
    
    if semantic_search_response.status_code == 200:
        semantic_search_results = semantic_search_response.json()['results']
    else:
        return semantic_search_response.json()['error'], 400
    
    full_text_search_request_body = {
        'query': query,
        'k': top_k * 2      # Fetching more results than required; will filter while responding
    }
    full_text_search_response = requests.post(f'{BACKEND_URL_PATH}/full-text-search', json=full_text_search_request_body)
    
    if full_text_search_response.status_code == 200:
        full_text_search_results = full_text_search_response.json()['results']
    else:
        return full_text_search_response.json()['error'], 400
    
    rrf_request_body = {
        'semantic_search_results': semantic_search_results,
        'full_text_search_results': full_text_search_results
    }
    rrf_response = requests.post(f'{BACKEND_URL_PATH}/rrf-results', json=rrf_request_body)
    
    if rrf_response.status_code == 200:
        rrf_results = rrf_response.json()['results']
    else:
        return rrf_response.json()['error'], 400
    
    rerank_request_body = {
        'query': query,
        'results': rrf_results
    }
    rerank_response = requests.post(f'{BACKEND_URL_PATH}/rerank-results', json=rerank_request_body)
    
    if rerank_response.status_code == 200:
        rerank_results = rerank_response.json()['results']
    else:
        return rerank_response.json()['error'], 400
    
    return jsonify({'results': rerank_results}), 200

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
    if 'semantic_search_results' not in request.json:
        return jsonify({'error': 'No semantic search results provided'}), 400
    
    if 'full_text_search_results' not in request.json:
        return jsonify({'error': 'No full-text search results provided'}), 400
    
    semantic_search_results = request.json['semantic_search_results']
    full_text_search_results = request.json['full_text_search_results']
    k = 60
    
    fused_results_mapping = {}
    fused_scores = defaultdict(float)
    for rank, result in enumerate(semantic_search_results, 1):
        fused_scores[result['id']] += 1 / (k + rank)
        fused_results_mapping[result['id']] = result
        
    for rank, result in enumerate(full_text_search_results, 1):
        fused_scores[result['id']] += 1 / (k + rank)
        fused_results_mapping[result['id']] = result
    
    fused_results = []
    for doc_id, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True):
        fused_results_mapping[doc_id]['score'] = score
        fused_results.append(fused_results_mapping[doc_id])
    
    return jsonify({'results': fused_results}), 200

@app.post('/rerank-results')
def rerank():
    from sentence_transformers import CrossEncoder
    import torch
    
    if 'query' not in request.json:
        return jsonify({'error': 'No query provided'}), 400
    
    if 'results' not in request.json:
        return jsonify({'error': 'No search results provided'}), 400
    
    query = request.json['query']
    results = request.json['results']
    
    print(f'{query = }')
    
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', default_activation_function=torch.nn.Sigmoid())
    rerank_inputs = []
    for result in results:
        rerank_inputs.append((query, result['content']))
    rerank_scores = reranker.predict(rerank_inputs)
    reranked_results = sorted(zip(results, rerank_scores), key=lambda x: x[1], reverse=True)
    for result, score in reranked_results:
        result['score'] = float(score)
    
    return jsonify({'results': [result[0] for result in reranked_results]}), 200


if __name__ == '__main__':
    get_store('vector').clear()
    get_store('text').clear()
    app.run(debug=True)