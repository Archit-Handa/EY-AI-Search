import requests

BACKEND_URL_PATH = 'http://127.0.0.1:5000'

def query(query, embedder_name, model_name, k):
    try:
        request_body = {
            'query': query,
            'embedder': embedder_name,
            'model': model_name,
            'k': k
        }

        response = requests.post(f'{BACKEND_URL_PATH}/query', json=request_body)

        if response.status_code == 200:
            return response.json()
        
        else:
            raise ValueError(response.json().get('error', 'Search failed'))
        
    except Exception as e:
        raise RuntimeError(f'Error in searching: {e}')
    
    
    