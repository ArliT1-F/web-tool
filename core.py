import os
import json
import socket
import requests
import argparse
from urllib.parse import urlparse
from datetime import datetime
from rich.console import Console
from rich.table import Table

from scanner.headers import analyze_headers, detect_waf
from scanner.ssl_analyzer import analyze_ssl
from scanner.vuln_check import check_known_vuln_paths
from scanner.spider import crawl_site
from scanner.extract import detect_ip_grabber, extract_links
from scanner.ip_tools import validate_target, get_whois_info
from scanner.virustotal import check_virustotal
from scanner.report import save_scan_report
from scanner.subdomains import brute_force_subdomains
from scanner.stack_fingerprint import fingerprint_tech_stack
from scanner.auth_scanner import find_login_forms
from scanner.dir_brute import brute_common_paths
from scanner.heuristics import detect_sqli_xss
from scanner.anti_bot import detect_bot_protection

console = Console()
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
SUBDOMAIN_WORDLIST = ["www", "mail", "admin", "test", "api", "dev"]
COMMON_PATHS = ["admin", "backup", ".git", "phpinfo.php", "config"]

def scan_website(url, fast_mode=False):
    console.rule(f"[bold cyan]Scanning {url}...")
    scan_summary = {"url": url, "datetime": str(datetime.now()), "reports": []}

    if not validate_target(url):
        console.print("[red]Target blocked or invalid.")
        scan_summary["error"] = "Target blocked"
        save_scan_report(scan_summary, f"scan_{urlparse(url).netloc}.json")
        return
    
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        body = response.text
        domain = urlparse(url).netloc
        
        
        scan_summary["headers"] = analyze_headers(headers)
        scan_summary["waf"] = detect_waf(headers)
        scan_summary["ssl"] = analyze_ssl(url)
        scan_summary["vulnerabilities"] = check_known_vuln_paths(url)
        
        if not fast_mode:
            scan_summary["subdomains"] = brute_force_subdomains(domain, SUBDOMAIN_WORDLIST)
            scan_summary["tech_stack"] = fingerprint_tech_stack(headers, body)
            scan_summary["auth_forms"] = find_login_forms(url)
            scan_summary["dir_brute"] = brute_common_paths(url, COMMON_PATHS)
            scan_summary["anti_bot"] = detect_bot_protection(headers, body)
    
    except Exception as e:
        console.print(f"[red]Scan failed: {e}")
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
            report["virustotal"] = check_virustotal(link) if not fast_mode else "skipped"
            report["whois"] = get_whois_info(link) if not fast_mode else "skipped"
            report["heuristics"] = detect_sqli_xss(link)
        try:
            report["ip"] = socket.gethostbyname(urlparse(link).netloc)
        except:
            report["ip"] = None
            scan_summary["reports"].append(report)

    save_scan_report(scan_summary, f"scan_{urlparse(url).netloc}.json")
    console.print(f"[green]\nScan completed. Report saved.\n")

    # Display summary table
    table = Table(title="Scan Summary")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    for k in ["ssl", "waf", "headers"]:
        v = scan_summary.get(k)
        if isinstance(v, dict):
            v = ", ".join(f"{i}: {j}" for i, j in v.items())
        table.add_row(k, str(v))
    console.print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Website Security Scanner")
    parser.add_argument("url", help="Target website URL")
    parser.add_argument("--fast", action="store_true", help="Skip slow scans like WHOIS, subdomains")
    args = parser.parse_args()
    scan_website(args.url, fast_mode=args.fast)