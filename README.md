# 🛡️ WebSecScan — Advanced Website Security Scanner

**WebSecScan** is a modular, extensible, and high-performance website security auditing tool written in Python. It performs deep scans on any public website — identifying vulnerabilities, technologies, misconfigurations, phishing traits, and more — and generates detailed, shareable reports.

---

## 🚀 Features

### 🔐 Core Security Scanning
- SSL/TLS certificate analysis
- Security headers check (CSP, HSTS, etc.)
- WAF/CDN detection (Cloudflare, Akamai, etc.)
- Directory & file brute-force (`admin`, `.git`, `phpinfo.php`)
- Login/auth form detection & HTTPS enforcement
- Subdomain enumeration (brute-force)

### 🧬 Technology Fingerprinting
- CMS & framework detection (WordPress, Joomla, Laravel, etc.)
- Language and server inference from headers and structure

### 📡 External Intelligence
- WHOIS lookups
- IP geolocation and ASN/ISP profiling
- VirusTotal API integration for live malware flagging
- CVE fingerprinting based on CMS/plugin detection

### 🧪 Active Vulnerability Testing
- Optional mode for testing input vectors (non-destructive)
- XSS & SQLi payload injection into:
  - URL query parameters
  - HTML form fields
- Detects reflection of payloads and vulnerable input points

### 🧠 Phishing & Obfuscation Detection
- Static analysis for suspicious JS code (`eval`, `atob`, `keylogger`)
- Phishing-like URL patterns (`login.php`, `secure-login`, etc.)
- Domain heuristics (length, hyphens, keyword matches)

### 📊 Risk Scoring Engine
- Final score (0–100) based on:
  - Missing headers
  - VirusTotal flags
  - CVEs
  - Suspicious scripts or phishing indicators
- Penalties included for detailed diagnostics

---

## 📤 Output Options

Generate and save reports in:
- **JSON** (default)
- **HTML**: `--output html`
- **Markdown**: `--output md`

Reports are saved under `/reports/`.  
Custom templates are in `/templates/`.

---

## 🧩 Plugin Support

Drop-in modules in the `plugins/` folder are automatically discovered and executed with `--use-plugins`.

Each plugin must export:
```python
def run_plugin(url, html, headers):
    return { "note": "Custom result" }
```

## 🧰 Command-Line Usage
```bash
websecscan https://example.com --output html --active --fast
```
### Avaliable Flags

| Flag             | Description                                           |
|------------------|-------------------------------------------------------|
| `--fast`         | Skip WHOIS, VirusTotal, and subdomain enumeration     |
| `--active`       | Run XSS/SQLi fuzzing on URLs and forms                |
| `--use-plugins`  | Load and execute any plugins found in `/plugins/`     |
| `--output`       | Choose report format: `json` (default), `html`, `md`  |

---
## 📦 Install Locally
```bash
git clone https://github.com/ArliT1-F/web-tool.git
cd websecscan
pip install .
```
Create an ```.env``` file in the root directory, and paste your VirusTotal API key:
```bash
VIRUSTOTAL_API_KEY="YOUR_API_KEY"
```

Then use it like:
```bash
websecscan https://example.com --output md
```
or
```bash
python3 websecscan.py https://example.com --output md --active
```
(just in case the first method doesnt work.)

---

## 🤝 Contributing
Pull requests, feature suggestions, and plugins are welcome!
Feel free to fork the project and submit your ideas, as I will be checking the project from time to time.

## 📜 License
MIT Licence
Built for security researchers, red teamers, and educators.

---

## ⚠️ Disclaimer
Use responsibly.
This tool is intended for **authorized testing only**.
Do not scan websites without permission.
