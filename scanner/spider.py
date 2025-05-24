from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

def crawl_site(url, depth=2):
    visited = set()
    to_visit = [(url, 0)]
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}

    while to_visit:
        current_url, current_depth = to_visit.pop(0)
        if current_depth > depth or current_url in visited:
            continue
        visited.add(current_url)

        try:
            resp = session.get(current_url, timeout=5, headers=headers)
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup.find_all("a", href=True):
                full_url = urljoin(current_url, tag["href"])
                if urlparse(full_url).netloc == urlparse(url).netloc:
                    to_visit.append((full_url, current_depth + 1))

        except:
            continue

    return visited
            