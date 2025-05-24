import socket
import re
from urllib.parse import urlparse
import whois

def validate_target(url):
    domain = urlparse(url).netloc
    try:
        ip = socket.gethostbyname(domain)
        if any(re.match(p, ip) for p in [r"^10\.\d+", r"^192\.168\.", r"^172\.(1[6-9]|2[0-9]|3[0-1])", r"^127\."]):
            return False
    
    except:
        return False
    return True

def get_whois_info(url):
    try:
        domain = urlparse(url).netloc
        return str(whois.query(domain)) or "No WHOIS info"
    except:
        return "WHOIS lookup failed"