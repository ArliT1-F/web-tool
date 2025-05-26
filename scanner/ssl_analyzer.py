import ssl
import socket
from urllib.parse import urlparse

def analyze_ssl(domain_or_url):
    try:
        # Extract netloc in case a full URL is provided
        parsed = urlparse(domain_or_url)
        host = parsed.netloc if parsed.netloc else domain_or_url

        # Strip port if present
        host = host.split(':')[0]

        # Validate DNS before SSL attempt
        socket.gethostbyname(host)

        context = ssl.create_default_context()
        with socket.create_connection((host, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                return {
                    "issuer": cert.get("issuer"),
                    "subject": cert.get("subject"),
                    "valid_from": cert.get("notBefore"),
                    "valid_to": cert.get("notAfter"),
                }
            
    except socket.gaierror:
        return {"error": "DNS resolution failed"}
    except Exception as e:
        return {"error": f"SSL analysis failed: {str(e)}"}
    