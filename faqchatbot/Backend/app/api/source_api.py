from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.source_model import Source

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("/")
def list_sources(db: Session = Depends(get_db)):
    """Lists all FAQ sources that have been scraped/ingested, with their status."""
    return db.query(Source).order_by(Source.created_at.desc()).all()


@router.get("/{source_id}")
def get_source(source_id: int, db: Session = Depends(get_db)):
    """Fetch details of a single ingested source by ID."""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.delete("/{source_id}")
def delete_source(source_id: int, db: Session = Depends(get_db)):
    """Remove a source record. Note: this does NOT delete its vectors from Pinecone."""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(source)
    db.commit()
    return {"status": "deleted", "id": source_id}