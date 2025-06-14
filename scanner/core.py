import os
import json
import socket
import requests
import argparse
import asyncio
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
from scanner.report import save_scan_report, export_html_report, export_md_report
from scanner.subdomains import brute_force_subdomains
from scanner.stack_fingerprint import fingerprint_tech_stack
from scanner.auth_scanner import find_login_forms
from scanner.dir_brute import brute_common_paths
from scanner.heuristics import detect_sqli_xss
from scanner.anti_bot import detect_bot_protection
from scanner.async_tools import extract_links_async, brute_force_subdomains_async, load_plugins, run_plugins
from scanner.profiling import get_host_profile, fingerprint_cves, calculate_risk_score
from scanner.active_tester import test_xss_sqli_in_url, test_xss_sqli_in_forms
from scanner.smart_detect import is_url_suspicious
from scanner.recon import fetch_robots_txt, fetch_sitemap_links, ScanSession

console = Console()
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
SUBDOMAIN_WORDLIST = ["www", "mail", "admin", "test", "api", "dev"]
COMMON_PATHS = ["admin", "backup", ".git", "phpinfo.php", "config"]

def convert_sets_to_lists(obj):
    if isinstance(obj, dict):
        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
    elif isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, list):
        return [convert_sets_to_lists(i) for i in obj]
    else:
        return obj

def scan_website(url, fast_mode=False, use_plugins=False, output_format="json", active_mode=False, auth_header=None, cookie_header=None):
    console.rule(f"[bold cyan]Scanning {url}...")
    scan_summary = {"url": url, "datetime": str(datetime.now()), "reports": []}
    session = ScanSession(auth_header=auth_header, cookie_header=cookie_header)

    if not validate_target(url):
        console.print("[red]Target blocked or invalid.")
        scan_summary["error"] = "Target blocked"
        domain = urlparse(url).netloc
        basename = f"scan_{domain}"
        output_path = f"reports/{basename}.{output_format}"

        if output_format == "html":
            result = export_html_report(scan_summary, output_path)
        elif output_format == "md":
            result = export_md_report(scan_summary, output_path)
        else:
            save_scan_report(scan_summary, output_path)
            result = True

        if result is True:
            console.print(f"[yellow]\nScan aborted. Report saved to {output_path}\n")
        else:
            console.print(f"[red]\nScan aborted, and report failed to save: {result}\n")
        return
    
    try:
        response = session.get(url)
        headers = response.headers
        body = response.text
        domain = urlparse(url).netloc
        
        
        scan_summary["headers"] = analyze_headers(headers)
        scan_summary["waf"] = detect_waf(headers)
        scan_summary["ssl"] = analyze_ssl(url)
        scan_summary["vulnerabilities"] = check_known_vuln_paths(url)
        
        if not fast_mode:
            subdomains = asyncio.run(brute_force_subdomains_async(domain, SUBDOMAIN_WORDLIST))
            scan_summary["subdomains"] = subdomains
            scan_summary["tech_stack"] = fingerprint_tech_stack(headers, body)
            scan_summary["auth_forms"] = find_login_forms(url)
            scan_summary["dir_brute"] = brute_common_paths(url, COMMON_PATHS)
            scan_summary["anti_bot"] = detect_bot_protection(headers, body)
            scan_summary["crawl"] = crawl_site(url)
            scan_summary["cve_matches"] = fingerprint_cves(scan_summary["tech_stack"])
            scan_summary["recon"] = {
                "robots_disallowed": fetch_robots_txt(url),
                "sitemap_links": fetch_sitemap_links(url)
            }

        if use_plugins:
            plugins = load_plugins()
            plugin_results = run_plugins(plugins, url, body, headers)
            scan_summary["plugins"] = plugin_results
    
    except Exception as e:
        console.print(f"[red]Scan failed: {e}")
        scan_summary["error"] = str(e)
        domain = urlparse(url).netloc
        basename = f"scan_{domain}"
        output_path = f"reports/{basename}.{output_format}"

        if output_format == "html":
            result = export_html_report(scan_summary, output_path)
        elif output_format == "md":
            result = export_md_report(scan_summary, output_path)
        else:
            save_scan_report(scan_summary, output_path)
            result = True

        if result is True:
            console.print(f"[yellow]\nScan aborted. Report saved to {output_path}\n")
        else:
            console.print(f"[red]\nScan aborted, and report failed to save: {result}\n")
        return
    
    all_links = list(asyncio.run(extract_links_async(url)))
    if not all_links:
        scan_summary["link_extraction_error"] = "No links found or crawling failed"
    
    for link in all_links:
        report = {"link": link}
        if detect_ip_grabber(link):
            report["ip_grabber"] = True
            report["virustotal"] = check_virustotal(link) if not fast_mode else "skipped"
            report["whois"] = get_whois_info(link) if not fast_mode else "skipped"
            report["heuristics"] = detect_sqli_xss(link)
            try:
                js_snippets = []
                resp = session.get(link)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, 'html.parser')
                for script in soup.find_all('script'):
                    if script.string:
                        js_snippets.appeend(script.string)
                report["suspicious_analysis"] = is_url_suspicious(link, js_snippets)
            except:
                report["suspicious_analysis"] = {"error": "Failed to analyze scripts"}
            
            
            if active_mode:
                report["active_tests"] = {
                    "xss_sqli_url": test_xss_sqli_in_url(link),
                    "xss_sqli_forms": test_xss_sqli_in_forms(link)
                }

        try:
            ip = socket.gethostbyname(urlparse(link).netloc)
            report["ip"] = ip
            report["host_profile"] = get_host_profile(ip)
            
        except:
            report["ip"] = None
            report["host_profile"] = {"error": "Could not resolve IP"}
            scan_summary["reports"].append(report)

    # Final risk score
    scan_summary["risk"] = calculate_risk_score(scan_summary)

    domain = urlparse(url).netloc
    basename = f"scan_{domain}"
    output_path = f"reports/{basename}.{output_format}"

    # Save in the requested format
    if output_format == "html":
        result = export_html_report(convert_sets_to_lists(scan_summary), output_path)
    elif output_format == "md":
        result = export_md_report(convert_sets_to_lists(scan_summary), output_path)
    else:
        save_scan_report(convert_sets_to_lists(scan_summary), output_path)
        result = True

    if result is True:
        console.print(f"[green]\nScan completed. Report saved to {output_path}\n")
    else:
        console.print(f"[red]\nScan completed, but report failed to save: {result}\n")
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

def main():
    parser = argparse.ArgumentParser(description="Website Security Scanner")
    parser.add_argument("url", help="Target website URL")
    parser.add_argument("--fast", action="store_true", help="Skip slow scans like WHOIS, subdomains")
    parser.add_argument("--use-plugins", action="store_true", help="Run additional plugins")
    parser.add_argument("--output", choices=["html", "md", "json"], default="json", help="Output report format (default: json)")
    parser.add_argument("--active", action="store_true", help="Run active XSS/SQLi fuzz tests.")
    parser.add_argument("--auth-header", help="Custom auth header (e.g., 'Authorization: Bearer xyz')")
    parser.add_argument("--cookie", help="Custom cookie header")
    args = parser.parse_args()
    
    
    scan_website(
        args.url,
        fast_mode=args.fast,
        use_plugins=args.use_plugins,
        output_format=args.output,
        active_mode=args.active,
        auth_header=args.auth_header,
        cookie_header=args.cookie
    )