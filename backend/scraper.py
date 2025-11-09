# scraper.py
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36"
}

def remove_reference_links(content_tag):
    for sup in content_tag.find_all("sup"): # Removing external links
        sup.decompose()
    return content_tag

def remove_tables(content_tag):
    for table in content_tag.find_all("table"): # Removing unnessesary tables
        table.decompose()
    return content_tag

def scrape_wikipedia(url):
    res = requests.get(url, headers=headers, timeout=10)    # Getting wikipedia raw data
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml") # Scraping using BeautifulSoup

    title_tag = soup.find("h1", id="firstHeading")  # Finding heading in scraped data
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    content_div = soup.find("div", id="mw-content-text")    # Finding contents in scraped data
    if not content_div:
        raise ValueError("Main content not found")

    content_div = remove_reference_links(content_div)
    content_div = remove_tables(content_div)
    # sections to exclude to avoid overhead to the AI model
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

    sections = []
    current_section = None
    current_subsection = None

    for element in content_div.find_all(["h2", "h3", "p", "ul"], recursive=True):
        # Handle new main section (h2)
        if element.name == "h2":
            # Get the raw section title (without [edit])
            heading_text = element.get_text(" ", strip=True).replace("[edit]", "").strip().lower()

            # If the previous section exists, append it before starting a new one
            if current_section and current_section["heading"].lower() not in EXCLUDED_SECTIONS:
                if current_subsection:
                    current_section["subsections"].append(current_subsection)
                    current_subsection = None
                sections.append(current_section)

            # Start a new section only if NOT excluded
            if heading_text not in EXCLUDED_SECTIONS:
                current_section = {"heading": heading_text.title(), "content": "", "subsections": []}
            else:
                current_section = None  # skip excluded section entirely

        # Handle subsections (h3)
        elif element.name == "h3" and current_section:
            subheading_text = element.get_text(" ", strip=True).replace("[edit]", "").strip().lower()
            if subheading_text not in EXCLUDED_SECTIONS:
                if current_subsection:
                    current_section["subsections"].append(current_subsection)
                current_subsection = {"subheading": subheading_text.title(), "content": ""}

        # Handle paragraph or list content
        elif element.name in ["p", "ul"]:
            text = element.get_text(" ", strip=True)
            if current_subsection:
                current_subsection["content"] += " " + text
            elif current_section:
                current_section["content"] += " " + text

    # Append last section at end
    if current_section and current_section["heading"].lower() not in EXCLUDED_SECTIONS:
        if current_subsection:
            current_section["subsections"].append(current_subsection)
        sections.append(current_section)
    return {"title": title, "sections": sections}


