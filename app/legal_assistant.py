import os
import faiss
import numpy as np

from openai import OpenAI
import pickle
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load embedding model
query_embedding = model.encode([query])

# Load FAISS index
index = faiss.read_index("legal_index.faiss")

# Load chunks (we must save them during ingestion)
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# OpenAI client
client = OpenAI()

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

def retrieve(query, k=5):
    query_embedding = get_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_embedding, k)

    results = []
    for i in indices[0]:
        results.append(chunks[i])
    return results

def generate_answer(query, retrieved_chunks):
    context = "\n\n".join(
        [f"Case ID: {chunk['source']}\n{chunk['text']}" for chunk in retrieved_chunks]
    )

    prompt = f"""
You are a legal assistant.

Answer ONLY using the provided legal context.
If answer not found, say: Information not available in documents.
Cite the Case ID in your answer.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    query = input("Ask a legal question: ")

    retrieved = retrieve(query)
    answer = generate_answer(query, retrieved)

    print("\n--- ANSWER ---\n")
    print(answer)