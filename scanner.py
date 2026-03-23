import requests
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scan_url(url):
    results = []

    try:
        res = requests.get(url, timeout=10, headers=HEADERS)
    except:
        return [{"name": "Site Unreachable", "severity": "Critical"}]

    # 1. Missing Security Headers
    required_headers = ["X-Frame-Options", "Content-Security-Policy", "X-XSS-Protection"]

    for h in required_headers:
        if h not in res.headers:
            results.append({
                "name": f"Missing Header: {h}",
                "severity": "Medium"
            })

    # 2. XSS Test
    try:
        payload = "<script>alert(1)</script>"
        r = requests.get(url + "?q=" + payload, headers=HEADERS)
        if payload in r.text:
            results.append({"name": "XSS Vulnerability", "severity": "High"})
    except:
        pass

    # 3. SQL Injection Test
    try:
        payload = "' OR '1'='1"
        r = requests.get(url + "?id=" + payload, headers=HEADERS)
        if "error" in r.text.lower():
            results.append({"name": "SQL Injection", "severity": "Critical"})
    except:
        pass

    # 4. Open Redirect
    try:
        r = requests.get(url + "?redirect=https://evil.com", allow_redirects=False, headers=HEADERS)
        if "Location" in r.headers:
            results.append({"name": "Open Redirect", "severity": "High"})
    except:
        pass

    # 5. Directory Listing
    try:
        r = requests.get(urljoin(url, "/"), headers=HEADERS)
        if "Index of" in r.text:
            results.append({"name": "Directory Listing Enabled", "severity": "Medium"})
    except:
        pass

    return results


def calculate_risk(results):
    score_map = {
        "Critical": 10,
        "High": 7,
        "Medium": 5,
        "Low": 3,
        "Informational": 1
    }

    return sum(score_map[r["severity"]] for r in results)