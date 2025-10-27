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

## 🚀 Run on GitHub (scheduled, auto-published reports)

Follow these steps to host the project on GitHub and keep it running on a schedule via GitHub Actions. Reports will be committed to a `gh-pages` branch and published with GitHub Pages.

### 1) Push this project to your GitHub repo
- Create a new repository on GitHub (public or private)
- From your local machine or CI environment:
```bash
git init
git add .
git commit -m "feat: initial import of WebSecScan"
git branch -M main
git remote add origin git@github.com:<your-username>/<your-repo>.git
git push -u origin main
```

### 2) Add your VirusTotal API key as a secret
- GitHub → Your repository → Settings → Secrets and variables → Actions → New repository secret
- Name: `VIRUSTOTAL_API_KEY`
- Value: your actual API key

### 3) Add a `targets.txt` file (domains you own)
- Create a file named `targets.txt` in the repo root containing one authorized URL per line, for example:
```text
https://example.com
https://sub.example.com
```

### 4) Add the GitHub Actions workflow
- Create the file `.github/workflows/websecscan.yml` with the following content:
```yaml
name: WebSecScan

on:
  schedule:
    - cron: "0 3 * * *"   # daily at 03:00 UTC
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: websecscan
  cancel-in-progress: true

jobs:
  scan:
    runs-on: ubuntu-latest
    env:
      VIRUSTOTAL_API_KEY: ${{ secrets.VIRUSTOTAL_API_KEY }}

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install WebSecScan
        run: |
          python -m pip install --upgrade pip
          pip install .

      - name: Run scans
        run: |
          mkdir -p reports
          TS=$(date -u +%Y%m%d_%H%M%S)
          while IFS= read -r url; do
            [ -z "$url" ] && continue
            websecscan "$url" --output html --fast || true
            dom=$(echo "$url" | sed 's|https\?://||; s|/||g')
            if [ -f "reports/scan_${dom}.html" ]; then
              mv "reports/scan_${dom}.html" "reports/${TS}_${dom}.html"
            fi
          done < targets.txt

      - name: Upload artifact (reports)
        uses: actions/upload-artifact@v4
        with:
          name: reports-${{ github.run_number }}
          path: reports/

      - name: Publish to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: reports
          keep_files: true
```

### 5) Enable GitHub Pages
- Repo → Settings → Pages → Build and deployment
- Source: `Deploy from a branch`
- Branch: `gh-pages`, Folder: `/ (root)`
- Save. Your reports will be available at `https://<your-username>.github.io/<your-repo>/`

### 6) Run it now
- Go to Actions → `WebSecScan` → Run workflow
- After it finishes, view the Pages site or download the artifact

### Notes and tips
- Only include domains you own or are authorized to scan in `targets.txt`.
- Remove `--fast` in the workflow to enable all checks (slower, more API use).
- To keep history, the workflow timestamps report filenames; adjust as needed.
- If you need private reports, skip GitHub Pages and rely on build artifacts only.
- For heavy scans or tighter control, consider a VPS + `cron`/`systemd` instead of Actions.

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
