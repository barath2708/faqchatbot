from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FAQChatbotScraper/1.0; +https://example.com/bot-info)"
}
REQUEST_TIMEOUT_SECONDS = 15


@dataclass
class ScrapedItem:
    source_url: str
    question: Optional[str]
    text: str


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.text


def scrape_faq_page(
    url: str,
    question_selector: Optional[str] = None,
    answer_selector: Optional[str] = None,
    fallback_content_selector: str = "body",
) -> list[ScrapedItem]:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    items: list[ScrapedItem] = []

    if question_selector and answer_selector:
        questions = soup.select(question_selector)
        answers = soup.select(answer_selector)

        if questions and answers and len(questions) == len(answers):
            for q_tag, a_tag in zip(questions, answers):
                question_text = q_tag.get_text(strip=True)
                answer_text = a_tag.get_text(separator=" ", strip=True)
                if question_text and answer_text:
                    items.append(ScrapedItem(url, question_text, answer_text))

    if not items:
        container = soup.select_one(fallback_content_selector) or soup
        text = container.get_text(separator="\n", strip=True)
        if text:
            items.append(ScrapedItem(url, None, text))

    return items


def scrape_multiple_pages(
    urls: list[str],
    question_selector: Optional[str] = None,
    answer_selector: Optional[str] = None,
) -> list[ScrapedItem]:
    all_items: list[ScrapedItem] = []
    for url in urls:
        try:
            all_items.extend(scrape_faq_page(url, question_selector, answer_selector))
        except requests.RequestException as exc:
            print(f"[scraper] Failed to scrape {url}: {exc}")
    return all_items


def _same_domain(base_url: str, candidate_url: str) -> bool:
    return urlparse(base_url).netloc == urlparse(candidate_url).netloc


def _extract_links(base_url: str, html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        full_url = urljoin(base_url, href)
        full_url = full_url.split("#")[0]
        if _same_domain(base_url, full_url):
            links.append(full_url)
    return links


def crawl_website(
    start_urls: list[str],
    question_selector: Optional[str] = None,
    answer_selector: Optional[str] = None,
    max_pages: int = 20,
) -> list[ScrapedItem]:
    visited: set[str] = set()
    queue: list[str] = list(dict.fromkeys(start_urls))
    all_items: list[ScrapedItem] = []

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            html = fetch_html(url)
        except requests.RequestException as exc:
            print(f"[crawler] Failed to fetch {url}: {exc}")
            continue

        soup = BeautifulSoup(html, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        page_items: list[ScrapedItem] = []
        if question_selector and answer_selector:
            questions = soup.select(question_selector)
            answers = soup.select(answer_selector)
            if questions and answers and len(questions) == len(answers):
                for q_tag, a_tag in zip(questions, answers):
                    question_text = q_tag.get_text(strip=True)
                    answer_text = a_tag.get_text(separator=" ", strip=True)
                    if question_text and answer_text:
                        page_items.append(ScrapedItem(url, question_text, answer_text))

        if not page_items:
            text = soup.get_text(separator="\n", strip=True)
            if text:
                page_items.append(ScrapedItem(url, None, text))

        all_items.extend(page_items)
        print(f"[crawler] Scraped ({len(visited)}/{max_pages}): {url}")

        try:
            new_links = _extract_links(url, html)
        except Exception as exc:
            print(f"[crawler] Failed to extract links from {url}: {exc}")
            new_links = []

        for link in new_links:
            if link not in visited and link not in queue:
                queue.append(link)

    return all_items