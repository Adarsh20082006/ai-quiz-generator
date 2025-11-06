# scraper.py
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36"
}

def remove_reference_links(content_tag):
    for sup in content_tag.find_all("sup"):
        sup.decompose()
    return content_tag

def remove_tables(content_tag):
    for table in content_tag.find_all("table"):
        table.decompose()
    return content_tag

def scrape_wikipedia(url):
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    title_tag = soup.find("h1", id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    content_div = soup.find("div", id="mw-content-text")
    if not content_div:
        raise ValueError("Main content not found")

    content_div = remove_reference_links(content_div)
    content_div = remove_tables(content_div)

    sections = []
    current_section = None
    current_subsection = None
    EXCLUDED_SECTIONS = {
    "see also",
    "notes",
    "references",
    "external links",
    "further reading",
    "citations",
    "bibliography",
    "footnotes",
    "sources"
    }
    for element in content_div.find_all(["h2", "h3", "p", "ul"], recursive=True):
        if element.name == "h2":
            if current_section and element.get_text(strip=True).lower() not in EXCLUDED_SECTIONS:
                if current_subsection:
                    current_section["subsections"].append(current_subsection)
                    current_subsection = None
                sections.append(current_section)
            current_section = {"heading": element.get_text(" ", strip=True), "content": "", "subsections": []}

        elif element.name == "h3":
            if current_subsection:
                current_section["subsections"].append(current_subsection)
            current_subsection = {"subheading": element.get_text(" ", strip=True), "content": ""}

        elif element.name == "p":
            text = element.get_text(" ", strip=True)
            if current_subsection:
                current_subsection["content"] += " " + text
            elif current_section:
                current_section["content"] += " " + text

        elif element.name == "ul":
            items = [li.get_text(" ", strip=True) for li in element.find_all("li")]
            text = "\n".join(f"• {i}" for i in items if i)
            if current_subsection:
                current_subsection["content"] += "\n" + text
            elif current_section:
                current_section["content"] += "\n" + text

    if current_subsection:
        current_section["subsections"].append(current_subsection)
    if current_section:
        sections.append(current_section)

    return {"title": title, "sections": sections}
