from transformers import pipeline
from config import *
import os

pipe = pipeline(
    "text-generation",
    model="models/llama-3.2-1b",
    model_kwargs={"local_files_only": True}
)

def generate_answer(question, context):
    prompt = f"""Context: {context}
Question: {question}
Answer: """
    
    # Most basic generation parameters
    response = pipe(prompt, max_new_tokens=128)[0]['generated_text']
    answer = response.split("Answer: ")[-1].strip()
    return answer