from app.services.pinecone_service import query_similar_chunks
from app.services.embedding_service import embed_text

question = "What is TensorFlow?"
embedding = embed_text(question)
results = query_similar_chunks(embedding, top_k=3)

for r in results:
    print("\n---")
    print(r)
