from sentence_transformers import SentenceTransformer
import numpy as np

# Load a pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample documents
documents = [
    open("quantnote.py","r").read(),
]

# Chunking and embedding
chunks = [doc.split('. ') for doc in documents]  # Simple split by sentences
flat_chunks = [sentence for sublist in chunks for sentence in sublist]
embeddings = model.encode(flat_chunks)

# Store embeddings for later retrieval
np.save('embeddings.npy', embeddings)
