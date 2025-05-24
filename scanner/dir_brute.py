import requests

def brute_common_paths(base_url, paths):
    found = []
    for p in paths:
        try:
            r = requests.get(base_url.rstrip("/") + "/" + p, timeout=5)
            if r.status_code == 200:
                found.append(p)
        except:
            continue
    return found