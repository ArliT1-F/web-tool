import requests
import os

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

def check_virustotal(url):
    if not API_KEY:
        return {"error": "No API key"}
    try:
        headers = {"x-apikey": API_KEY}
        res = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": url})
        if res.status_code != 200:
            return {"error": res.status_code}
        scan_id = res.json()["data"]["id"]
        result = requests.get(f"https://www.virustotal.com/api/v3/analyses/{scan_id}", headers=headers)
        return result.json()
    except Exception as e:
        return {"error": str(e)}