import os
from .embeddings import query_vector_db
import openai

def answer_question(question, collection):
    # Retrieve docs
    docs = query_vector_db(collection, question, top_k=3)
    context = " ".join([doc for doc in docs['documents'][0]])
    sources = [meta['source'] for meta in docs['metadatas'][0]]
    # Simple prompt (can be improved for your LLM)
    prompt = f"Answer the question using this context from KIIT docs:\n{context}\nQuestion: {question}\nAnswer:"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # Use your model choice
        messages=[{"role": "system", "content": "KIIT college assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.1,
    )
    answer = completion.choices[0].message.content
    return answer, sources
