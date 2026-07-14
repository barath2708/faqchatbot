"""
Prompt for extracting topic keywords from a chunk of text, used to
populate the Neo4j knowledge graph during ingestion.
"""

TOPIC_EXTRACTION_PROMPT = """Extract 2 to 4 short topic keywords (1-3 words each) that best represent
the subject matter of the text below. Return ONLY a comma-separated list,
nothing else. No explanations, no numbering.

Text:
{text}
"""


def build_topic_extraction_prompt(text: str) -> list[dict]:
    return [
        {"role": "user", "content": TOPIC_EXTRACTION_PROMPT.format(text=text)},
    ]