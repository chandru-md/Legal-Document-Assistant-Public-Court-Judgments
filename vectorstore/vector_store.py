import faiss
import numpy as np

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index

def save_index(index, path="legal_index.faiss"):
    faiss.write_index(index, path)

'''def retrieve(query, model, index, chunks, k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)

    results = []
    for i in indices[0]:
        results.append(chunks[i])

    return results

query = "What was the main constitutional issue?"
results = retrieve(query, model, index, chunks)

for r in results:
    print("Source:", r["source"])
    print("Text snippet:", r["text"][:300])
    print("-" * 50)

if __name__ == "__main__":

    import os
    import faiss
    import numpy as np

    # Absolute path to raw data
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FOLDER = os.path.abspath(
        os.path.join(BASE_DIR, "..", "raw_data", "constitutional")
    )

    print("Loading documents...")
    documents = load_documents(DATA_FOLDER)
    print(f"Loaded {len(documents)} documents")

    print("Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks")

    print("Generating embeddings...")
    embeddings = generate_embeddings(chunks)
    print(f"Embeddings shape: {embeddings.shape}")

    print("Creating FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    print("Saving FAISS index...")
    faiss.write_index(index, "legal_index.faiss")

    print("Vector store created successfully.")'''