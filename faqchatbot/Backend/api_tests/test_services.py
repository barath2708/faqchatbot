import os
from dotenv import load_dotenv

load_dotenv()

print("\n--- Testing Pinecone ---")
try:
    from pinecone import Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    indexes = pc.list_indexes()
    print("✅ Pinecone connected. Indexes:", [i.name for i in indexes])
except Exception as e:
    print("❌ Pinecone failed:", e)

print("\n--- Testing Gemini (Embeddings) ---")
try:
    from google import genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    result = client.models.embed_content(model="gemini-embedding-001", contents="hello world")
    print("✅ Gemini connected. Embedding length:", len(result.embeddings[0].values))
except Exception as e:
    print("❌ Gemini failed:", e)

print("\n--- Testing Groq (LLM) ---")
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say hello in 3 words"}]
    )
    print("✅ Groq connected. Response:", response.choices[0].message.content)
except Exception as e:
    print("❌ Groq failed:", e)

print("\n--- Testing Neo4j ---")
try:
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
    )
    driver.verify_connectivity()
    print("✅ Neo4j connected")
except Exception as e:
    print("❌ Neo4j failed:", e)

print("\n--- Testing Redis ---")
try:
    import redis
    r = redis.from_url(os.getenv("REDIS_URL"))
    r.ping()
    print("✅ Redis connected")
except Exception as e:
    print("❌ Redis failed:", e)

print("\nDone.\n")
