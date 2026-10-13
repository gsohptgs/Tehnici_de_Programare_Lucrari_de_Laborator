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
    if path.startswith("/"):
        return f"https://{host}{path}"
    return f"https://{host}/{path}"


def is_https(url):
    return url.startswith("https://")


def show_response(url):
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
    except requests.RequestException:
        print("Status: Eroare conexiune")


def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown")
        }
    except requests.RequestException as e:
        return {"status": None, "error": f"Eroare: {type(e).__name__}"}


def scan_sites():
    results = []
    
    for url in SITES:
        result = check_site(url)
        result["url"] = url 
        results.append(result)
        
    reusite_200 = [r for r in results if r.get("status") == 200]
    reusite_200.sort(key=lambda x: x.get("length", 0), reverse=True)
    
    for r in reusite_200:
        print(f"{r['url']} -> {r['status']}, {r['length']} octeți")
        
    reusite_total = len([r for r in results if r.get("status") is not None])
    esuate_total = len(results) - reusite_total
    
    print(f"\nReușite: {reusite_total} Eșuate: {esuate_total}")


def check_headers(url):
    try:
        response = requests.get(url, timeout=5)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        
        present = []
        missing = []
        
        for header in SECURITY_HEADERS:
            if header.lower() in headers_lower:
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
        return {"status": None, "error": f"Eroare: {type(e).__name__}"}


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
            last_status = None
            last_error = f"Eroare: {type(e).__name__}"
            
    result = {"status": last_status, "attempts": attempts}
    if last_status is None and last_error:
        result["error"] = last_error
        
    return result