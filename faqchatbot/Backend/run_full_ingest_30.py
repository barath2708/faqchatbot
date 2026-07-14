from app.services.ingestion_pipeline import ingest_website
import time

start = time.time()
result = ingest_website(
    urls=["https://www.tensorflow.org/"],
    crawl=True,
    max_pages=30,
    extract_topics=False,
)
print("\nRESULT:", result)
print(f"Took {time.time() - start:.1f} seconds")
