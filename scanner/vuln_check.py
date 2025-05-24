import requests

def check_known_vuln_paths(base_url):
    paths = ["/.git/", "/.admin/", "/phpinfo.php", "/.env/"]
    findings = {}
    for path in paths:
        try:
            r = requests.get(base_url.rstrip("/") + path, timeout=5)
            if r.status_code == 200:
                findings[path] = "Exposed"

        except:
            continue
    return findings