import logging
from openai import OpenAI
from app.config import settings
from app.prompts.faq_prompt import build_prompt

logger = logging.getLogger(__name__)
_client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

def generate_answer(question: str, context_chunks: list[dict]) -> str:
    try:
        messages = build_prompt(question, context_chunks)
        response = _client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Could not generate answer from LLM: {e}")
        if not context_chunks:
            return f"I don't have any information about: {question}. Please check that FAQ data has been ingested."
        return f"I encountered an error while generating an answer. Please try again."


def correct_question_spelling(question: str) -> str:
    """
    Uses the LLM to fix typos/spelling in the user's question before
    embedding + search, without changing its meaning.
    """
    try:
        response = _client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Fix any spelling or typing mistakes in the user's question. "
                                "Keep the meaning and technical terms (like TensorFlow, Keras, TFX) exactly as intended. "
                                "Return ONLY the corrected question, nothing else — no explanation, no quotes."
                },
                {"role": "user", "content": question},
            ],
            temperature=0.0,
        )
        corrected = response.choices[0].message.content.strip()
        return corrected if corrected else question
    except Exception as e:
        logger.warning(f"Could not correct question spelling: {e}")
        return question