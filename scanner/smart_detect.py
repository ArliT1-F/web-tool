import re
from urllib.parse import urlparse

# 🚨 Patterns that hint at phishing or credential theft
SUSPICIOUS_DOMAINS = [
    r"login.*\.(php|html)",   # login.php, login.html
    r"account.*",             # account verification
    r"verify.*",              # verify identity
    r"secure.*",              # secure-login
    r"bank.*",                # bank of fake
    r"paypal.*"               # PayPal phishing
]

# 🚩 JavaScript behavior that is commonly obfuscated or dangerous
SUSPICIOUS_JS_KEYWORDS = [
    "eval(", "atob(", "setInterval(", "document.write(", "decodeURIComponent(",
    "steal", "track", "logkeys", "keylogger", "csrf", "payload", "webhook"
]

def score_url_heuristics(url):
    """Detect suspicious domain structure or keywords in the URL."""
    flags = []
    domain = urlparse(url).netloc.lower()

    # Heuristics
    if len(domain) > 40:
        flags.append("Unusually long domain name")
    if "-" in domain:
        flags.append("Domain contains hyphens (commonly used to spoof legit domains)")

    for pattern in SUSPICIOUS_DOMAINS:
        if re.search(pattern, url, re.IGNORECASE):
            flags.append(f"Matches phishing pattern: '{pattern}'")

    return flags

def score_js_heuristics(js_code):
    """Detect dangerous JavaScript patterns."""
    flags = []
    for keyword in SUSPICIOUS_JS_KEYWORDS:
        if keyword.lower() in js_code.lower():
            flags.append(f"Suspicious JS keyword: {keyword}")
    return flags

def is_url_suspicious(url, js_snippets=None):
    """Combine all heuristics and return a verdict."""
    js_snippets = js_snippets or []
    reasons = score_url_heuristics(url)

    for js in js_snippets:
        reasons += score_js_heuristics(js)

    return {
        "is_suspicious": bool(reasons),
        "suspicion_reasons": reasons
    }
