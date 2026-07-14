from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.source_model import Source
from app.services.ingestion_pipeline import ingest_website

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