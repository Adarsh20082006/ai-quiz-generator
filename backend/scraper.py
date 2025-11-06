import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def remove_reference_links(content_tag):
    for sup in content_tag.find_all("sup", class_="reference"):
        sup.decompose()
    return content_tag

def remove_tables(content_tag):
    """Remove info tables and infoboxes"""
    for table in content_tag.find_all("table"):
        table.decompose()
    return content_tag


def scrape_wikipedia(url: str):
    res = requests.get(url, headers=headers, timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    title_tag = soup.find("h1", id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled Article"

    content_div = soup.find("div", id="mw-content-text")
    if not content_div:
        raise ValueError("Could not find main content")

    content_div = remove_reference_links(content_div)
    content_div = remove_tables(content_div)

    sections = []
    current_section = None
    current_subsection = None

    for element in content_div.find_all(["h2", "h3", "p", "ul"], recursive=True):
        # Stop at non-article sections
        if element.name in ["h2", "h3"]:
            heading_text = element.get_text(" ", strip=True)
            if any(x in heading_text.lower() for x in ["see also", "references", "external", "notes", "further reading"]):
                break

        if element.name == "h2":
            if current_section:
                if current_subsection:
                    current_section["subsections"].append(current_subsection)
                    current_subsection = None
                # Clean empty content if only subsections exist
                if not current_section.get("content") and current_section["subsections"]:
                    current_section.pop("content", None)
                sections.append(current_section)

            current_section = {
                "heading": heading_text,
                "content": "",
                "subsections": []
            }

        elif element.name == "h3":
            if current_subsection and current_section:
                current_section["subsections"].append(current_subsection)

            current_subsection = {
                "subheading": heading_text,
                "content": ""
            }

        elif element.name == "p":
            text = element.get_text(" ", strip=True)
            if text:
                if current_subsection:
                    current_subsection["content"] += " " + text
                elif current_section:
                    current_section["content"] += " " + text
                else:
                    sections.insert(0, {
                        "heading": "Introduction",
                        "content": text,
                        "subsections": []
                    })

        elif element.name == "ul":
            # Extract bullet points
            items = []
            for li in element.find_all("li", recursive=False):
                # Combine text from <a> and plain text
                item_text = li.get_text(" ", strip=True)
                if item_text:
                    items.append("• " + item_text)

            if items:
                joined_list = "\n".join(items)
                if current_subsection:
                    current_subsection["content"] += "\n" + joined_list
                elif current_section:
                    current_section["content"] += "\n" + joined_list

    # Close last open section/subsection
    if current_subsection and current_section:
        current_section["subsections"].append(current_subsection)
    if current_section:
        if not current_section.get("content") and current_section["subsections"]:
            current_section.pop("content", None)
        sections.append(current_section)

    return {
        "title": title,
        "sections": sections
    }
