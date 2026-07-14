import re

BOILERPLATE_PATTERNS = [
    r"accept all cookies",
    r"we use cookies.*?privacy policy",
    r"subscribe to our newsletter",
    r"all rights reserved",
    r"skip to (main )?content",
]

_BOILERPLATE_REGEX = re.compile("|".join(BOILERPLATE_PATTERNS), flags=re.IGNORECASE | re.DOTALL)


def clean_text(raw_text: str) -> str:
    text = _strip_control_characters(raw_text)
    text = _remove_boilerplate(text)
    text = _collapse_whitespace(text)
    text = _dedupe_lines(text)
    return text.strip()


def _strip_control_characters(text: str) -> str:
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)


def _remove_boilerplate(text: str) -> str:
    return _BOILERPLATE_REGEX.sub("", text)


def _collapse_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _dedupe_lines(text: str) -> str:
    lines = text.split("\n")
    deduped = []
    previous = None
    for line in lines:
        stripped = line.strip()
        if stripped != previous:
            deduped.append(line)
        previous = stripped
    return "\n".join(deduped)