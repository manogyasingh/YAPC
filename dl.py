# download_model.py
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import *

def download_model():
    print("Downloading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B", token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B", token=HF_TOKEN)
    print("Download complete!")

if __name__ == "__main__":
    download_model()
