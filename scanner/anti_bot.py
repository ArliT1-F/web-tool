def detect_bot_protection(headers, body):
    indicators = []
    if "captcha" in body.lower():
        indicators.append("Captcha detected")
    if any(h in headers for h in ["cf-ray", "x-sucuri-id", "x-akamai"]):
        indicators.append("WAF/CDN protection")
    return indicators