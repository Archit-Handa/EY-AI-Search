from .base import Embedder
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIEmbedder(Embedder):
    def __init__(self, model_name: str='text-embedding-ada-002'):
        self.model_name = model_name
        self.api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.api_version = os.getenv('AZURE_OPENAI_API_VERSION')
        self.api_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        
        if not all([self.api_key, self.api_version, self.api_endpoint]):
            raise ValueError('Missing OpenAI API configuration. Ensure AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, and AZURE_OPENAI_ENDPOINT are set.')
        
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.api_endpoint
        )
        
    def _embed(self, input: list[str]) -> list[list[float]]:
        try:
            response = self.client.embeddings.create(input=input, model=self.model_name)
            return [data.embedding for data in response.data]
        
        except Exception as e:
            raise RuntimeError(f'Error embedding text with OpenAI: {e}')