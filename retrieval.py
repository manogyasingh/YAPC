from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from config import *

model = SentenceTransformer(VECTOR_MODEL)

def load_vectordb():
    embeddings = np.load(CACHE_DIR / 'embeddings.npy')
    chunks = np.load(CACHE_DIR / 'chunks.npy')
    index = faiss.read_index(str(CACHE_DIR / 'faiss.index'))
    return index, chunks

def get_relevant_chunks(query, index, chunks, top_k=TOP_K):
    query_embedding = model.encode([query])
    query_embedding = query_embedding.astype(np.float32)
    query_embedding = query_embedding / np.linalg.norm(query_embedding)
    
    scores, indices = index.search(query_embedding, top_k)
    relevant_chunks = chunks[indices[0]]
    return relevant_chunks.tolist()