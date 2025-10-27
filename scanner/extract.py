from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin
import requests

def extract_links(url):
    try:
        session = requests.Session()
        resp = session.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        links = {urljoin(url, tag.get("href")) for tag in soup.find_all("a", href=True) if isinstance(tag, Tag)}
        return links, None
    except Exception as e:
        return set(), str(e)
    

def detect_ip_grabber(url):
    import re
    patterns = [r'\d{10,}', r'[a-zA-Z]{20,}', r'[0-9a-f]{32}']
    domains = ["grabify.link", "iplogger.org", "ipgrabber.io"]
    return any(re.search(p, url) for p in patterns) or any(d in url for d in domains)