from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

def find_login_forms(url):
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        forms = soup.find_all("form")
        results = []
        for form in forms:
            inputs = form.find_all("input")
            if any(i.get("type") == "password" for i in inputs):
                results.append({
                    "action": urljoin(url, form.get("action", "")),
                    "method": form.get("method", "get")
                })
        return results
    except:
        return []