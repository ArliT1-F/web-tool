import re

def detect_sqli_xss(url):
    issues = []
    if re.search(r"\?.*=.*('|\"|%27|%22)", url):
        issues.append("Potential SQL Injection")
    if re.search(r"<script>|%3Cscript%3E", url, re.IGNORECASE):
        issues.append("Potential XSS Attack")
    return issues