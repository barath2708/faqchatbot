from app.services.ingestion_pipeline import ingest_website
import time

start = time.time()
result = ingest_website(
    urls=["https://www.tensorflow.org/"],
    crawl=True,
    max_pages=100,
    extract_topics=False,   # avoid Groq rate-limit stalls; can re-enable later in smaller batches
)
print("\nRESULT:", result)
print(f"Took {time.time() - start:.1f} seconds")