from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chat_model import ChatLog
from app.models.feedback_model import Feedback
from app.services.cache_service import get_cached_answer, set_cached_answer
from app.services.embedding_service import embed_text
from app.services.pinecone_service import query_similar_chunks, query_by_topics
from app.services.neo4j_service import extract_topics, get_related_topics
from app.services.llm_service import generate_answer, correct_question_spelling

router = APIRouter(prefix="/question", tags=["question"])


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    chat_log_id: int
    answer: str
    sources: list[str]
    from_cache: bool


class FeedbackRequest(BaseModel):
    chat_log_id: int
    is_helpful: bool
    comment: str | None = None


@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest, db: Session = Depends(get_db)):
    corrected_question = correct_question_spelling(request.question)

    cached = get_cached_answer(corrected_question)
    if cached:
        log = ChatLog(
            question=corrected_question,
            answer=cached["answer"],
            source_urls=",".join(cached.get("sources", [])),
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return QuestionResponse(**cached, from_cache=True, chat_log_id=log.id)

    query_embedding = embed_text(corrected_question)
    vector_matches = query_similar_chunks(query_embedding, top_k=5)

    question_topics = extract_topics(corrected_question)
    related_topics: list[str] = []
    for topic in question_topics:
        related_topics.extend(get_related_topics(topic, limit=3))
    related_topics = list(set(related_topics) - set(question_topics))

    graph_matches = query_by_topics(related_topics, top_k=3) if related_topics else []

    combined = {m["text"]: m for m in vector_matches}
    for m in graph_matches:
        combined.setdefault(m["text"], m)
    all_matches = list(combined.values())

    answer = generate_answer(corrected_question, all_matches)
    sources = list({m["source_url"] for m in all_matches if m["source_url"]})

    result = {"answer": answer, "sources": sources}
    set_cached_answer(corrected_question, result)

    log = ChatLog(
        question=corrected_question,
        answer=answer,
        source_urls=",".join(sources),
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return QuestionResponse(**result, from_cache=False, chat_log_id=log.id)


@router.post("/feedback")
def submit_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    chat_log = db.query(ChatLog).filter(ChatLog.id == request.chat_log_id).first()
    if not chat_log:
        raise HTTPException(status_code=404, detail="chat_log_id not found")

    feedback = Feedback(
        chat_log_id=request.chat_log_id,
        is_helpful=request.is_helpful,
        comment=request.comment,
    )
    db.add(feedback)
    db.commit()

    return {"status": "ok"}