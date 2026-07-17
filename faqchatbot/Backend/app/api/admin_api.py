from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.models.source_model import Source
from app.services.ingestion_pipeline import ingest_website
from app.services.sitemap_service import analyze_site, analyze_site_deep
from app.services.job_tracker import create_job, update_job, get_job

router = APIRouter(prefix="/admin", tags=["admin"])


class ScrapeRequest(BaseModel):
    urls: list[str] = Field(...)
    question_selector: str | None = Field(default=None)
    answer_selector: str | None = Field(default=None)
    crawl: bool = Field(default=False, description="If true, follow same-domain links starting from urls")
    max_pages: int = Field(default=20, description="Maximum number of pages to crawl when crawl=true")


class ScrapeResponse(BaseModel):
    pages_scraped: int
    chunks_created: int
    topics_extracted: int
    status: str


class BulkScrapeRequest(BaseModel):
    urls: list[str] = Field(...)


class AnalyzeSiteRequest(BaseModel):
    url: str = Field(...)


@router.post("/scrape", response_model=ScrapeResponse)
def scrape_faq_source(request: ScrapeRequest, db: Session = Depends(get_db)):
    if not request.urls:
        raise HTTPException(status_code=400, detail="At least one URL is required")

    result = ingest_website(
        urls=request.urls,
        question_selector=request.question_selector,
        answer_selector=request.answer_selector,
        crawl=request.crawl,
        max_pages=request.max_pages,
    )

    for url in request.urls:
        source = db.query(Source).filter(Source.url == url).first()
        if not source:
            source = Source(url=url)
            db.add(source)
        source.status = result["status"]
        source.chunks_created = result["chunks_created"]
    db.commit()

    return ScrapeResponse(**result)


@router.post("/analyze-site")
def analyze_site_endpoint(request: AnalyzeSiteRequest):
    return analyze_site(request.url)


@router.post("/analyze-site-deep")
def analyze_site_deep_endpoint(request: AnalyzeSiteRequest):
    return analyze_site_deep(request.url)


def _run_bulk_scrape(job_id: str, urls: list[str]):
    db = SessionLocal()
    total_chunks = 0

    for i, url in enumerate(urls):
        update_job(job_id, current_url=url)
        try:
            result = ingest_website(urls=[url], question_selector=None, answer_selector=None)

            source = db.query(Source).filter(Source.url == url).first()
            if not source:
                source = Source(url=url)
                db.add(source)
            source.status = result["status"]
            source.chunks_created = result["chunks_created"]
            db.commit()

            total_chunks += result["chunks_created"]
        except Exception as e:
            update_job(job_id, error=f"Failed on {url}: {str(e)}")
            # continue to next page rather than stopping the whole job

        update_job(job_id, pages_done=i + 1, chunks_created=total_chunks)

    update_job(job_id, status="completed", current_url=None)
    db.close()


@router.post("/scrape-bulk-async")
def scrape_bulk_async(request: BulkScrapeRequest, background_tasks: BackgroundTasks):
    if not request.urls:
        raise HTTPException(status_code=400, detail="No URLs provided")

    job_id = create_job(total_pages=len(request.urls))
    background_tasks.add_task(_run_bulk_scrape, job_id, request.urls)
    return {"job_id": job_id, "total_pages": len(request.urls)}


@router.get("/scrape-status/{job_id}")
def scrape_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job