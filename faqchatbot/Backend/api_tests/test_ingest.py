from app.services.ingestion_pipeline import ingest_website
import time

start = time.time()
result = ingest_website(
    urls=["https://www.tensorflow.org/guide"],
    crawl=False,
    max_pages=1,
)
print("\nRESULT:", result)
print(f"Took {time.time() - start:.1f} seconds")
