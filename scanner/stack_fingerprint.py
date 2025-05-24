import re

def fingerprint_tech_stack(headers, html):
    stack = {}
    server = headers.get("Server", "Unknown")
    powered = headers.get("X-Powered-By", "Unknown")
    stack["server"] = server
    stack["x_powered_by"] = powered

    if "django" in powered.lower():
        stack["framework"] = "Django"
    elif "laravel" in powered.lower():
        stack["framework"] = "Laravel"
    elif "flask" in powered.lower():
        stack["framework"] = "Flask"
    elif "express" in powered.lower():
        stack["framework"] = "Express.js"
    
    if re.search(r"\.php", html):
        stack["language"] = "PHP"
    elif re.search(r"\.py", html):
        stack["language"] = "Python"
    elif re.search(r"\.js", html):
        stack["language"] = "JavaScript"

    return stack