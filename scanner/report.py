import os
import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Setup Jinja2 environment once, resolving templates
PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE_DIR = PACKAGE_DIR / "templates"
template_loader = FileSystemLoader(str(DEFAULT_TEMPLATE_DIR))
env = Environment(loader=template_loader)


def export_html_report(scan_data, output_path):
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path) or "."
        os.makedirs(output_dir, exist_ok=True)

        template = env.get_template("report_template.html")
        rendered = template.render(scan=scan_data)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        return True
    except Exception as e:
        return f"HTML export failed: {e}"
    
def export_md_report(scan_data, output_path):
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path) or "."
        os.makedirs(output_dir, exist_ok=True)

        template = env.get_template("report_template.md")
        rendered = template.render(scan=scan_data)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        return True
    except Exception as e:
        return f"Markdown export failed: {e}"

def save_scan_report(data, filename):
    output_dir = os.path.dirname(filename) or "."
    os.makedirs(output_dir, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved to {filename}")