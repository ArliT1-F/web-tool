def analyze_headers(headers):
    important = [
        "Content-Security-Policy",
        "X-Content-Type-Options",
        "Strict-Transport-Security",
        "X-Frame-Options"
    ]
    return {h: headers.get(h, "Missing") for h in important}

def detect_waf(headers):
    waf_keys = ["Server", "X-CDN", "CF-RAY", "X-Sucuri-ID", "X-Akamai"]
    return {k: headers[k] for k in waf_keys if k in headers}
