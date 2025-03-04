from .base import Embedder
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIEmbedder(Embedder):
    def __init__(self, model_name: str='text-embedding-ada-002'):
        self.model_name = model_name
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key: raise ValueError('OpenAI API Key is missing. Set it as an environment variable: OPENAI_API_KEY')
        
        openai.api_key = self.api_key
        
    def _embed(self, input: list[str]) -> list[list[float]]:
        try:
            response = openai.Embedding.create(input=input, model=self.model_name)
            return [data['embedding'] for data in response['data']]
        
        except Exception as e:
            print(f'OpenAI API Error: {e}')
            return []