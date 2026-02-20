import re
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

import faiss
import numpy as np
from vectorstore.vector_store import create_faiss_index, save_index
import pickle
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    text = re.sub(r'Page \d+', '', text)  # remove page numbers if any
    return text.strip()



def load_documents(folder_path):
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            documents.append({
                "text": text,
                "source": filename.replace(".txt", "")
            })

    return documents



def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1400,
        chunk_overlap=300
    )

    chunks = []

    for doc in documents:
        split_texts = splitter.split_text(doc["text"])

        for chunk in split_texts:
            chunks.append({
                "text": chunk,
                "source": doc["source"]
            })

    return chunks


client = OpenAI()

def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["text"]
        )
        embeddings.append(emb.data[0].embedding)
    return np.array(embeddings)



def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index

def retrieve(query, model, index, chunks, k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)

    results = [chunks[i] for i in indices[0]]
    return results

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FOLDER = os.path.abspath(
    os.path.join(BASE_DIR, "..", "raw_data", "constitutional")
    )

    documents = load_documents(DATA_FOLDER)
    print(f"Loaded {len(documents)} documents")

    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks")

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print("Chunks saved successfully.")

    embeddings = generate_embeddings(chunks)
    print(f"Embeddings shape: {embeddings.shape}")

    index = create_faiss_index(embeddings)
    print("FAISS index created")

    save_index(index)
    print("Index saved successfully")
