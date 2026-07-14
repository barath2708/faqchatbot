from app.services.embedding_service import embed_text
from app.services.pinecone_service import query_similar_chunks
from app.services.llm_service import generate_answer

question = "What is TensorFlow?"

embedding = embed_text(question)
chunks = query_similar_chunks(embedding, top_k=3)

print(f"\nFound {len(chunks)} relevant chunks\n")

answer = generate_answer(question, chunks)

print("ANSWER:\n")
print(answer)
