from langchain.tools import tool
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

def _fetch_page_text(url: str) -> str:
    """Download webpage content and return clean text."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        return "I found a result but could not retrieve its webpage content."

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove script and style tags
    for tag in soup(["script", "style"]):
        tag.extract()

    text = " ".join(soup.get_text(separator=" ").split())

    # Limit to 1000 chars for readability
    return text[:1200] + "..." if len(text) > 1200 else text


@tool("web_search", return_direct=False)
def web_search(query: str) -> str:
    """
    Searches DuckDuckGo and returns readable content from the top result.
    
    Use this when the user wants:
    - real-time information
    - answers requiring web browsing
    - summaries of web pages

    Input: natural language search query
    """
    with DDGS() as ddgs:
        results = ddgs.text(query, region="us-en", max_results=5)
        results_list = list(results)

    if not results_list:
        return f"No results found for: {query}"

    # Prefer Wikipedia if available
    wiki = next((r for r in results_list if "wikipedia.org" in r["href"]), results_list[0])

    title = wiki["title"]
    url = wiki["href"]

    page_text = _fetch_page_text(url)

    return (
        
        # f"🔍 **Search Query:** {query}\n"
        f"Certainly maam, here's the top result for: \"{query}\"\n\n"
        # f"🏷 **Top Result:** {title}\n"
        # f"🔗 **URL:** {url}\n\n"
        f"📄 **Extracted Content:**\n{page_text}"
    )


# if __name__ == "__main__":
#     print(web_search.func("How many continents are there?"))

