import socket

def brute_force_subdomains(domain, wordlist):
    found = []
    for sub in wordlist:
        fqdn = f"{sub}.{domain}"
        try:
            socket.gethostbyname(fqdn)
            found.append(fqdn)
        except:
            continue
    return found