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
{% if scan.tech_stack is defined and scan.tech_stack %}
{% for tech in scan.tech_stack %}
- {{ tech }}
{% endfor %}
{% else %}
- None detected
{% endif %}

---

## 📌 CVE Matches
{% if scan.cve_matches is defined and scan.cve_matches %}
{% for k, v in scan.cve_matches.items() %}
- **{{ k }}:** {{ v | join(", ") }}
{% endfor %}
{% else %}
- None
{% endif %}

---

## 📁 Sensitive Paths Found
{% if scan.dir_brute is defined and scan.dir_brute %}
{% for path in scan.dir_brute %}
- `{{ path }}`
{% endfor %}
{% else %}
- None
{% endif %}

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
