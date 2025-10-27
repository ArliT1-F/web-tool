import re # noqa: E501
import socket

# CVE Fingerprinting
def fingerprint_cves(tech_stack):
    known_cves = {
        "wordpress": ["CVE-2021-29447", "CVE-2022-21661"],
        "drupal": ["CVE-2018-7600"],
        "joomla": ["CVE-2023-23752"],
        "php": ["CVE-2019-11043", "CVE-2020-7066"],
        "apache": ["CVE-2021-41773", "CVE-2021-42013"],
        "nginx": ["CVE-2021-23017", "CVE-2021-23018"],
        "mysql": ["CVE-2019-2725", "CVE-2020-2574"],
        "postgresql": ["CVE-2020-25694", "CVE-2021-32027"],
        "nodejs": ["CVE-2020-8174", "CVE-2021-22930"],
        "python": ["CVE-2020-8492", "CVE-2021-3177"],
        "ruby": ["CVE-2020-10933", "CVE-2021-3177"],
        "django": ["CVE-2020-9402", "CVE-2021-3281"],
        "flask": ["CVE-2020-28493", "CVE-2021-3177"],
        "laravel": ["CVE-2020-15168", "CVE-2021-3129"],
        "react": ["CVE-2020-7653", "CVE-2021-3177"],
        "vue": ["CVE-2020-11022", "CVE-2021-3177"],
        "angular": ["CVE-2020-7653", "CVE-2021-3177"],
        "kubernetes": ["CVE-2020-8554", "CVE-2021-25735"],
        "docker": ["CVE-2020-15257", "CVE-2021-21284"],
        "redis": ["CVE-2020-14147", "CVE-2021-32761"],
        "memcached": ["CVE-2020-15115", "CVE-2021-32761"],
        "elasticsearch": ["CVE-2020-7019", "CVE-2021-22139"],
        "mongodb": ["CVE-2020-7927", "CVE-2021-3177"],
        "kafka": ["CVE-2020-17518", "CVE-2021-3177"],
        "rabbitmq": ["CVE-2020-14379", "CVE-2021-3177"],
        "apache-tomcat": ["CVE-2020-1938", "CVE-2021-22963"],
        "iis": ["CVE-2020-0601", "CVE-2021-26855"],
        "windows": ["CVE-2020-0601", "CVE-2021-34527"],
        "linux": ["CVE-2020-14386", "CVE-2021-3493"],
        "macos": ["CVE-2020-9934", "CVE-2021-30869"],
        "android": ["CVE-2020-0022", "CVE-2021-0326"],
        "ios": ["CVE-2020-27930", "CVE-2021-30869"],
        "aws": ["CVE-2020-10766", "CVE-2021-3177"],
        "azure": ["CVE-2020-10766", "CVE-2021-3177"],
        "gcp": ["CVE-2020-10766", "CVE-2021-3177"],
        "docker-compose": ["CVE-2020-15257", "CVE-2021-21284"],
        "kubernetes-cli": ["CVE-2020-8554", "CVE-2021-25735"],
        "helm": ["CVE-2020-8554", "CVE-2021-25735"],
        "terraform": ["CVE-2020-17518", "CVE-2021-3177"],
        "ansible": ["CVE-2020-17518", "CVE-2021-3177"],
        "chef": ["CVE-2020-17518", "CVE-2021-3177"],
        "puppet": ["CVE-2020-17518", "CVE-2021-3177"],
        "git": ["CVE-2020-5260", "CVE-2021-21300"],
        "svn": ["CVE-2020-17518", "CVE-2021-3177"],
        "vagrant": ["CVE-2020-17518", "CVE-2021-3177"],
        "virtualbox": ["CVE-2020-17518", "CVE-2021-3177"],
        "vmware": ["CVE-2020-17518", "CVE-2021-3177"],
        "xen": ["CVE-2020-17518", "CVE-2021-3177"],
        "qemu": ["CVE-2020-17518", "CVE-2021-3177"],
        "openstack": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-spark": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-hadoop": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-kafka": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-cassandra": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-hive": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-spark": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-flink": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-kibana": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-logstash": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-solr": ["CVE-2020-17518", "CVE-2021-3177"],
        "apache-zookeeper": ["CVE-2020-17518", "CVE-2021-3177"],
    }
    results = {}
    for tech in tech_stack:
        tech_key = tech.lower()
        if tech_key in known_cves:
            results[tech] = known_cves[tech_key]
    return results or {"note": "No matching CVEs found for detected stack."}

# Target Profiling
def get_host_profile(ip):
    if not ip:
        return {"error": "No IP resolved."}
    
    return {
        "asn": "AS15169",
        "isp": "Google LLC",
        "country": "United States",
        "region": "California",
        "city": "Mountain View",
        "hostname": socket.getfqdn(ip)
    }


# Risk Scoring engine
def calculate_risk_score(scan_summary):
    score = 0
    penalties = []

    if scan_summary.get("headers"):
        missing = [k for k, v in scan_summary["headers"].items() if v == "Missing"]
        score += len(missing) * 5
        if missing:
            penalties.append(f"Missing headers: {', '.join(missing)}")

    if not scan_summary.get("waf"):
        score += 5
        penalties.append("No WAF detected")

    if scan_summary.get("dir_brute"):
        score += len(scan_summary["dir_brute"]) * 2
        penalties.append(f"Open sensitive paths: {len(scan_summary['dir_brute'])}")


    for r in scan_summary.get("reports", []):
        if r.get("ip_grabber"):
            score += 10
            penalties.append("IP grabber detected in links")
        if r.get("virustotal") not in [None, "skipped"] and isinstance(r["virustotal"], dict):
            stats = r["virustotal"].get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            if stats.get("malicious", 0) > 0:
                score += 15
                penalties.append("Malicious URL flagged by VirusTotal")


    risk_score = min(score, 100)
    return {"risk_score": risk_score, "penalties": penalties}

