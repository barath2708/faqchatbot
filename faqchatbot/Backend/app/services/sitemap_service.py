import httpx
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree
from bs4 import BeautifulSoup

WORDS_PER_CHUNK_ESTIMATE = 225  # ~300 tokens ≈ 225 words, matches CHUNK_SIZE_TOKENS
BYTES_PER_CHUNK_ESTIMATE = 10 * 1024  # ~10KB per stored chunk (vector + metadata)


def _fetch_sitemap_urls(sitemap_url: str, seen: set[str] | None = None) -> list[str]:
    if seen is None:
        seen = set()
    if sitemap_url in seen:
        return []
    seen.add(sitemap_url)

    resp = httpx.get(sitemap_url, timeout=15, follow_redirects=True)
    resp.raise_for_status()

    root = ElementTree.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    urls: list[str] = []

    # Case 1: sitemap INDEX file (points to other sitemaps)
    sub_sitemaps = root.findall("sm:sitemap/sm:loc", ns)
    if sub_sitemaps:
        for loc in sub_sitemaps:
            urls.extend(_fetch_sitemap_urls(loc.text.strip(), seen))
        return urls

    # Case 2: regular sitemap (lists actual pages)
    for loc in root.findall("sm:url/sm:loc", ns):
        urls.append(loc.text.strip())

    return urls


def analyze_site(base_url: str) -> dict:
    """Quick check: how many pages does this site's sitemap list?"""
    parsed = urlparse(base_url)
    domain = f"{parsed.scheme}://{parsed.netloc}"
    sitemap_url = urljoin(domain, "/sitemap.xml")

    try:
        all_urls = _fetch_sitemap_urls(sitemap_url)
    except Exception as e:
        return {
            "domain": domain,
            "sitemap_found": False,
            "error": str(e),
            "total_pages": 0,
            "sample_urls": [],
            "all_urls": [],
        }

    same_domain_urls = sorted(set(u for u in all_urls if urlparse(u).netloc == parsed.netloc))

    return {
        "domain": domain,
        "sitemap_found": True,
        "total_pages": len(same_domain_urls),
        "sample_urls": same_domain_urls[:20],
        "all_urls": same_domain_urls,
    }


def _extract_word_count(url: str) -> int:
    try:
        resp = httpx.get(url, timeout=10, follow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return len(text.split())
    except Exception:
        return 0


def analyze_site_deep(base_url: str, max_pages: int = 200) -> dict:
    """Full check: fetches every page's real text, counts words, estimates chunks/storage."""
    basic = analyze_site(base_url)
    if not basic["sitemap_found"]:
        return basic

    urls_to_check = basic["all_urls"][:max_pages]

    total_words = 0
    pages_analyzed = 0
    pages_failed = 0

    for url in urls_to_check:
        words = _extract_word_count(url)
        if words > 0:
            total_words += words
            pages_analyzed += 1
        else:
            pages_failed += 1

    estimated_chunks = round(total_words / WORDS_PER_CHUNK_ESTIMATE) if total_words else 0
    estimated_storage_kb = round((estimated_chunks * BYTES_PER_CHUNK_ESTIMATE) / 1024)

    return {
        "domain": basic["domain"],
        "sitemap_found": True,
        "total_pages_in_sitemap": basic["total_pages"],
        "pages_analyzed": pages_analyzed,
        "pages_failed": pages_failed,
        "total_word_count": total_words,
        "estimated_total_chunks": estimated_chunks,
        "estimated_storage_kb": estimated_storage_kb,
        "estimated_storage_mb": round(estimated_storage_kb / 1024, 2),
    }