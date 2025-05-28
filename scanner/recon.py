import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# +++ Authenticated session manager +++
class ScanSession:
    def __init__(self, auth_header=None, cookie_header=None):
        self.session = requests.Session()
        self.headers = {}

        # Custom auth header like: "Authorization: Bearer <token>"
        if auth_header:
            name, value = auth_header.split(":", 1)
            self.headers[name.strip()] = value.strip()

        # Custom Cookie header like: "session=abc123"
        if cookie_header:
            self.headers["Cookie"] = cookie_header.strip()

        self.session.headers.update(self.headers)

    def get(self, url, **kwargs):
        return self.session.get(url, timeout=10, **kwargs)
    
    def post(self, url, data=None, **kwargs):
        return self.session.post(url, data=data, timeout=10, **kwargs)
    

# robots.txt parser
def fetch_robots_txt(base_url):
    robots_url = urljoin(base_url, "/robots.txt")
    disallowed = []
    try:
        resp = requests.get(robots_url, timeout=5)
        if resp.status_code == 200:
            for line in resp.text.splitlines():
                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    disallowed.append(path)
    except:
        pass
    return disallowed


# sitemap.xml parser
def fetch_sitemap_links(base_url):
    sitemap_url = urljoin(base_url, "/sitemap.xml")
    links = []
    try:
        resp = requests.get(sitemap_url, timeout=5)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "xml")
            for loc in soup.find_all("loc"):
                links.append(loc.text.strip())
    except:
        pass
    return links