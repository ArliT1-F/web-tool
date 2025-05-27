# 🛡️ WebSecScan Report

**Target:** {{ scan.url }}  
**Scan Time:** {{ scan.datetime }}

---

## 🔐 SSL Certificate
{% for k, v in scan.ssl.items() %}
- **{{ k }}:** {{ v }}
{% endfor %}

---

## 🧱 WAF Detection
**WAF:** {{ scan.waf or 'None detected' }}

---

## 📑 Security Headers
{% for k, v in scan.headers.items() %}
- **{{ k }}:** {{ v }}
{% endfor %}

---

## 🧬 Tech Stack
{% for tech in scan.tech_stack %}
- {{ tech }}
{% endfor %}

---

## 📌 CVE Matches
{% for k, v in scan.cve_matches.items() %}
- **{{ k }}:** {{ v | join(", ") }}
{% endfor %}

---

## 📁 Sensitive Paths Found
{% for path in scan.dir_brute %}
- `{{ path }}`
{% endfor %}

---

## 📊 Risk Score
**Score:** {{ scan.risk.risk_score }}/100  
{% for reason in scan.risk.penalties %}
- ⚠️ {{ reason }}
{% endfor %}

---

## 🔗 Links Analyzed
{% for r in scan.reports %}
### {{ r.link }}
{% if r.ip_grabber %}
> ⚠️ Possible IP grabber
{% endif %}
- **IP:** {{ r.ip }}
- **WHOIS:** {{ r.whois }}
- **Heuristics:** {{ r.heuristics }}
{% endfor %}
