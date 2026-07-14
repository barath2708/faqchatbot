from fastapi import APIRouter
from pydantic import BaseModel
from app.services.cache_service import get_cached_answer, set_cached_answer
from app.services.embedding_service import embed_text
from app.services.pinecone_service import query_similar_chunks, query_by_topics
from app.services.neo4j_service import extract_topics, get_related_topics
from app.services.llm_service import generate_answer, correct_question_spelling  # ← add this import

router = APIRouter(prefix="/question", tags=["question"])

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    sources: list[str]
    from_cache: bool

@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    # --- Fix typos/spelling before anything else ---
    corrected_question = correct_question_spelling(request.question)  # ← add this line

    # --- CAG: check cache first ---
    cached = get_cached_answer(corrected_question)  # ← use corrected_question instead of request.question
    if cached:
        return QuestionResponse(**cached, from_cache=True)

    # --- RAG: vector similarity search ---
    query_embedding = embed_text(corrected_question)  # ← use corrected_question
    vector_matches = query_similar_chunks(query_embedding, top_k=5)

    # --- KAG: find related topics, pull in extra chunks tagged with them ---
    question_topics = extract_topics(corrected_question)  # ← use corrected_question
    related_topics: list[str] = []
    for topic in question_topics:
        related_topics.extend(get_related_topics(topic, limit=3))
    related_topics = list(set(related_topics) - set(question_topics))

    graph_matches = query_by_topics(related_topics, top_k=3) if related_topics else []

    combined = {m["text"]: m for m in vector_matches}
    for m in graph_matches:
        combined.setdefault(m["text"], m)
    all_matches = list(combined.values())

    # --- Generate answer using fused context ---
    answer = generate_answer(corrected_question, all_matches)  # ← use corrected_question
    sources = list({m["source_url"] for m in all_matches if m["source_url"]})

    result = {"answer": answer, "sources": sources}
    set_cached_answer(corrected_question, result)  # ← use corrected_question
    return QuestionResponse(**result, from_cache=False)