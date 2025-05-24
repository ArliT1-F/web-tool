import ssl
import socket

def analyze_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return {
                    "issuer": cert.get("issuer"),
                    "subject": cert.get("subject"),
                    "valid_from": cert.get("notBefore"),
                    "valid_until": cert.get("notAfter")
                }
    except Exception as e:
        return {"error": str(e)}