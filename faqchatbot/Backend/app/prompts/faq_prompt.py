SYSTEM_PROMPT = """You are a helpful FAQ assistant. Answer the user's question using ONLY the
context provided below. If the answer isn't in the context, say you don't know
rather than guessing. Keep answers clear and concise.

Context:
{context}
"""


def build_prompt(question: str, context_chunks: list[dict]) -> list[dict]:
    """
    Builds the messages array sent to the LLM, injecting retrieved
    context chunks (from Pinecone) into the system prompt so answers
    are grounded in your actual FAQ content.
    """
    context_text = "\n\n".join(
        f"[Source: {c['source_url']}]\n{c['text']}" for c in context_chunks
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context_text)},
        {"role": "user", "content": question},
    ]