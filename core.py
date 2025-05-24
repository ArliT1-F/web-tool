import os
import json
import socket
import requests
from urllib.parse import urlparse
from datetime import datetime

from scanner.headers import analyze_headers, detect_waf
from scanner.ssl_analyzer import analyze_ssl
from scanner.vuln_check import check_known_vuln_paths
from scanner.spider import crawl_site
from scanner.extract import detect_ip_grabber, extract_links
from scanner.ip_tools import validate_target, get_whois_info
from scanner.virustotal import check_virustotal
from scanner.report import save_scan_report

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

def scan_website(url):
    print(f"\n Starting scan: {url}")
    scan_summary = {"url": url, "datetime": str(datetime.now()), "reports": []}

    if not validate_target(url):
        scan_summary["error"] = "Target blocked"
        save_scan_report(scan_summary, f"scan_{urlparse(url).netloc}.json")
        return
    
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        domain = urlparse(url).netloc
        scan_summary["headers"] = analyze_headers(headers)
        scan_summary["waf"] = detect_waf(headers)
        scan_summary["ssl"] = analyze_ssl(url)
        scan_summary["vulnerabilities"] = check_known_vuln_paths(url)
    except Exception as e:
        scan_summary["error"] = str(e)
        save_scan_report(scan_summary, f"scan_{urlparse(url).netloc}.json")
        return
    all_links, error = extract_links(url)
    if error:
        scan_summary["link_extraction_error"] = error
    
    for link in all_links:
        report = {"link": link}
        if detect_ip_grabber(link):
            report["ip_grabber"] = True
        report["virustotal"] = check_virustotal(link)
        report["whois"] = get_whois_info(link)
        try:
            report["ip"] = socket.gethostbyname(urlparse(link).netloc)
        except:
            report["ip"] = None
            scan_summary["reports"].append(report)

    save_scan_report(scan_summary, f"scan_{urlparse(url).netloc}.json")

if __name__ == "__main__":
    while True:
        website = input("Enter website URL (or 'end' to exit): )").strip()
        if website.lower() in ["end", "cls", "clear"]:
            break
        scan_website(website)