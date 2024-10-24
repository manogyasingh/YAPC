from retrieval import load_vectordb, get_relevant_chunks
from llm import generate_answer

index, chunks = load_vectordb()
print("Vector database loaded successfully!")

while True:
    query = input("\nEnter your question: ")
    if query == 'q': break
        
    relevant_chunks = get_relevant_chunks(query, index, chunks)
    context = " ".join(relevant_chunks)
    
    answer = generate_answer(query, context)
    print(f"\nAnswer: {answer}")