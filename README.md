# 🔍 WebSecScan — Advanced Website Security Scanner

**WebSecScan** is a modular, extensible, and high-performance website security auditing tool written in Python. It performs deep scans on any public website, revealing security headers, WAF presence, CMS technologies, open directories, and more — with optional support for plugins, CVE mapping, and asynchronous crawling.

---

## 🚀 Features

### ✅ Core Security Scanning
- 🔐 SSL/TLS certificate analysis
- 📑 Security headers check (CSP, HSTS, etc.)
- 🧱 WAF/CDN detection (Cloudflare, Akamai, etc.)
- 🧭 Deep link crawling with `asyncio`
- 🧬 Technology stack fingerprinting (CMS, language, server)
- 🔍 Directory & file brute-force (e.g., `.git`, `admin`, `phpinfo.php`)
- 🔐 Login/authentication form detection

### 🧠 Intelligence Layer
- 🕵️ CVE fingerprinting (WordPress, Joomla, etc.)
- 🌍 IP profiling (ASN, ISP, region, hostname)
- 🧮 Risk scoring engine (0–100) based on observed vulnerabilities
- 🧪 VirusTotal scan integration
- 🧠 Heuristic analysis for IP grabbers, obfuscated scripts, potential XSS/SQLi

### 🧰 Tools & Extensibility
- ⚡ Asynchronous scanning for subdomains, links, and endpoints
- 🔌 Plugin system (`plugins/`) for drop-in scan modules
- 📤 Save reports in JSON, with support for HTML/Markdown exports
- 🎨 Rich CLI with summary tables

---

## 📦 Installation

```bash
git clone https://github.com/your-username/websecscan.git
cd websecscan
pip install -r requirements.txt
```

## ⚙️ Usage
```bash
python3 core.py https://example-website.com
```
Create an ```.env``` file in the root directory, and paste your VirusTotal API key:
```bash
VIRUSTOTAL_API_KEY="YOUR_API_KEY"
```
#### *Options*
```bash
---fast       Skip heavy scans(VirusTotal, WHOIS, subdomains)
---plugins    Run custom plugin modules from plugins/
---output     Choose report format (json, html, md)
```

## 📁 Report Structure
Each scan creates a report under ```/reports/```, e.g.:
```json
{
  "url": "https://example.com",
  "headers": {
    "Content-Security-Policy": "Missing",
    ...
  },
  "ssl": { "issuer": "...", "valid_until": "..." },
  "tech_stack": ["PHP", "Apache"],
  "risk": {
    "risk_score": 60,
    "penalties": ["Missing headers", "IP grabber found"]
  },
  ...
}
```
Run with ```--plugins``` to activate it.


## 🧪 Coming Soon
- 🔫 Active vulnerability testing (XSS, SQLi fuzzing)
- 📊 HTML/Markdown export with charts
- 📅 Cron/scheduled scanning with audit history

## 🤝 Contributing
Pull requests, feature suggestions, and plugins are welcome!
Feel free to fork the project and submit your ideas.

## 📜 License
MIT License.
Built with ❤️ for ethical hacking and education.

## 🛡 Disclaimer
This tool is intended for **authorized testing only**.
Do not scan websites without permission.
