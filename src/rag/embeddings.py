import chromadb
from chromadb.utils import embedding_functions

def create_vector_db(kiit_chunks, persist_dir="./data/processed"):
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection("kiit_docs")
    openai_embed = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="text-embedding-ada-002"
    )
  
    # Add documents if not exists
    
    for idx, doc in enumerate(kiit_chunks):
        collection.add(
            documents=[doc["text"]],
            metadatas=[{"source": doc["source"]}],
            ids=[str(idx)],
            embeddings=None, # Will use embed_fn automatically if None
        )
    return collection

def query_vector_db(collection, question, top_k=3):
    # Use OpenAI embedding for question
    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )
    return results
