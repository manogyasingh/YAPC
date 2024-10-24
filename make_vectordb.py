from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
from pathlib import Path
from config import *

model = SentenceTransformer(VECTOR_MODEL)

def chunk_text(text, chunk_size, overlap):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(' '.join(words[start:end]))
        start += chunk_size - overlap
    return chunks

def read_documents(data_dir):
    documents = []
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            documents.append(f.read())
    return documents

documents = read_documents(DATA_DIR)
all_chunks = []

for doc in documents:
    chunks = chunk_text(doc, CHUNK_SIZE, CHUNK_OVERLAP)
    all_chunks.extend(chunks)

embeddings = model.encode(all_chunks, show_progress_bar=True)
embeddings = embeddings.astype(np.float32)
embeddings = embeddings / np.linalg.norm(embeddings, axis=1)[:, np.newaxis]

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

np.save(CACHE_DIR / 'embeddings.npy', embeddings)
np.save(CACHE_DIR / 'chunks.npy', np.array(all_chunks))

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, str(CACHE_DIR / 'faiss.index'))