from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
VECTOR_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = os.path.join("models", "llama-3.2-1b")  # local for now
DATA_DIR = Path("./database")
CACHE_DIR = Path("./vectordb")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3
MAX_LENGTH = 2048
    
HF_TOKEN = os.getenv('HUGGINGFACE_TOKEN')  