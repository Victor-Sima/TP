import requests

SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    if not path.startswith("/"):
        path = "/" + path
    return f"https://{host}{path}"


def is_https(url):
    return url.startswith("https://")


def show_response(url):
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")


def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        content_type = response.headers.get("Content-Type", "")
        if ";" in content_type:
            content_type = content_type.split(";")[0].strip()
            
        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown")
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(type(e).__name__)}


def scan_sites():
    results = []
    for site in SITES:
        res = check_site(site)
        results.append((site, res))
        
    successful = [item for item in results if item[1].get("status") == 200]
    failed_count = len(results) - len(successful)
    
    successful.sort(key=lambda x: x[1].get("length", 0), reverse=True)
    
    for site, res in successful:
        print(f"{site} -> 200, {res['length']} octeți")
        
    print(f"Reușite: {len(successful)} Eșuate: {failed_count}")


def check_headers(url):
    try:
        response = requests.get(url, timeout=5)
        resp_headers = {k.lower(): v for k, v in response.headers.items()}
        
        present = []
        missing = []
        
        for header in SECURITY_HEADERS:
            if header.lower() in resp_headers:
                present.append(header)
            else:
                missing.append(header)
                
        score = int((len(present) / len(SECURITY_HEADERS)) * 100)
        
        return {
            "present": present,
            "missing": missing,
            "score": score
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(type(e).__name__)}


def retry_check(url, attempts=3):
    last_status = None
    last_error = None
    
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            
            if last_status < 500:
                return {"status": last_status, "attempts": attempt}
        except requests.RequestException as e:
            last_error = str(type(e).__name__)
            last_status = None
            
    result = {"status": last_status, "attempts": attempts}
    if last_error:
        result["error"] = last_error
    return result
