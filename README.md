# AI Search - EY
**AI Search in Documents capability for EY**

## About the Solution
This solution aims to process a document (PDF, DOCX, TXT, JSON) that is input and apply Hybrid Search (Semantic + Full-text Search with a Cross-Encoder) to retreieve the most relevant chunks from the document.

## Process
The process for the search is as follow:
1. Load the Doument and extract the text
2. Split the extracted text into smaller chunks
3. Embed the chunks into feature vectors using an Embedding Model
4. Store the chunks on ElasticSearch and their embeddings on Azure CosmosDB
5. Take the query string from the user
6. Embed the string into query vector using same embedding model
7. Retrive Semantic Search results from the embeddings stored on Azure CosmosDB based on cosine similarity
8. Retreive Full-text Search results from the chunks stored on ElasticSearch
9. Take the results from both searches and apply Reciprocal Rank Fusion (RRF) to rank the results
10. Use a Cross-Encoder to rerank the results based on the query and return the final results

## Current Support
Currently, the solution supports foolowing:
- Documents and their Loaders: PDF, Docx, Txt, Json
- Document Fetchers: Upload a document from local directory or Azure Blob Storage
- Chunkers: Page-level, Paragraph-level, Sentence-level, Fixed-width
- Embedding Models: SentenceTransformer's SBERT Models, OpenAI's Embedding Models

However, these are easily extensible by implementing the corresponding `base` classes.

## Running the solution
Before running the application, make sure to create a `.env` file in the `search/` directory and define the following environment variables:

```.env
AZURE_OPENAI_API_KEY="YOUR-OPENAI-API_KEY"
AZURE_OPENAI_API_VERSION="2024-10-21" or "YOUR-OPENAI-API-VERSION"
AZURE_OPENAI_ENDPOINT="YOUR-OPENAI-ENDPOINT"
COSMOSDB_CONNECTION_STRING="YOUR-COSMOSDB-CONNECTION-STRING"
COSMOSDB_DATABASE_NAME="Vector-Store" or "YOUR-COSMOS-DATABASE-NAME"
```

To run the application, execute the following command:

```bash
bash runner.sh
```

Once the application is running, you can visit [http://localhost:8501](http://localhost:8501) to use the application on a Streamlit interface. The Flask Backend runs on [http://localhost:5000](http://localhost:5000)

---

By: [Archit Handa](https://www.github.com/Archit-Handa), [Sparsh Aggarwal](https://github.com/sparsh0303)