import os
import json
from jinja2 import Environment, FileSystemLoader

template_loader = FileSystemLoader('./templates')
env = Environment(loader=template_loader)

# Setup Jinja2 environment
template_loader = FileSystemLoader("./templates")
env = Environment(loader=template_loader)


def export_html_report(scan_data, output_path):
    try:
        template = env.get_template("report_template.html")
        rendered = template.render(scan=scan_data)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        return True
    except Exception as e:
        return f"HTML export failded: {e}"
    
def export_md_report(scan_data, output_path):
    try:
        template = env.get_template("report_template.md")
        rendered = template.render(scan=scan_data)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        return True
    except Exception as e:
        return f"Markdown export failed: {e}"

def save_scan_report(data, filename):
    os.makedirs("reports", exist_ok=True)
    with open(os.path.join("reports", filename), "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved to reports/{filename}")