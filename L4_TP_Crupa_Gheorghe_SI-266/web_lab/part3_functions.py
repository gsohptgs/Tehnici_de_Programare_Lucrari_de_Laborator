# Laborator: funcții, metode și importuri pe web
# Student: <Crupa Gheorghe>

import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 21 & 23
def fetch(url, timeout=10):
    """Returnează obiectul răspuns HTTP pentru adresa url."""
    return requests.get(url, timeout=timeout)

# Exercițiul 22 & 26
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = fetch(url)
    return response.status_code

# Exercițiul 24 & 25
def get_title(html):
    """Primește un șir HTML și returnează textul din tag-ul <title>."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return None

# Exercițiul 27
def page_exists(url):
    """Returnează True dacă cererea reușește, False dacă dă o eroare de rețea."""
    try:
        fetch(url)
        return True
    except requests.RequestException:
        return False

# Exercițiul 28
def check_paths(base, paths):
    """Verifică mai multe rute pe un domeniu și returnează un dicționar cu codurile de stare."""
    results = {}
    for path in paths:
        url = base.rstrip("/") + "/" + path.lstrip("/")
        results[path] = get_status(url)
        time.sleep(1)
    return results

# Exercițiul 29
def get_header(url, name, default="lipsește"):
    """Extrage un antet specific din răspunsul unei cereri."""
    response = fetch(url)
    return response.headers.get(name, default)

# Exercițiul 30
def security_headers(url):
    """Verifică prezența a 5 antete de securitate."""
    response = fetch(url)
    headers_to_check = [
        "Strict-Transport-Security", "Content-Security-Policy",
        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"
    ]
    return {h: h in response.headers for h in headers_to_check}

# Exercițiul 31
def score_headers(results):
    """Calculează un scor de tip 'X/Y' pentru antete securizate."""
    score = sum(1 for val in results.values() if val)
    return f"{score}/{len(results)}"

# Exercițiul 32
def fetch_robots(base):
    """Descarcă fișierul robots.txt."""
    url = base.rstrip("/") + "/robots.txt"
    try:
        r = fetch(url)
        if r.status_code == 200:
            return r.text
        return None
    except requests.RequestException:
        return None

def disallowed_paths(robots_text):
    """Returnează lista rutelor Disallow din textul robots.txt."""
    if not robots_text:
        return []
    return [line.split(":", 1)[1].strip() for line in robots_text.splitlines() if line.startswith("Disallow:")]

# Exercițiul 33
def response_times(*urls):
    """Returnează dicționar cu timpi de răspuns."""
    times = {}
    for url in urls:
        r = fetch(url)
        times[url] = r.elapsed.total_seconds()
        time.sleep(1)
    return times

# Exercițiul 34
def log(message, **details):
    """Printează un mesaj log împreună cu argumentele cheie date."""
    details_str = " | ".join([f"{k}={v}" for k, v in details.items()])
    print(f"{message} | {details_str}")

# Bloc de rulare și testare exerciții partea 3:
if __name__ == "__main__":
    print("Ex21:", fetch(BASE_URL).status_code)
    time.sleep(1)
    print("Ex22 /:", get_status(BASE_URL + "/"))
    time.sleep(1)
    print("Ex22 /robots.txt:", get_status(BASE_URL + "/robots.txt"))
    time.sleep(1)
    print("Ex22 /sitemap.xml:", get_status(BASE_URL + "/sitemap.xml"))
    
    print("Ex24 Titlu:", get_title(fetch(BASE_URL).text))
    # help(get_title)  # ex 25
    get_status(123)  # ex 26 (Type hints nu ne opresc la rulare, ridică excepție pe intern sau funcționează cu coercie de tip)
    
    print("Ex27 Există domeniul fals?", page_exists("https://this-domain-does-not-exist.invalid"))
    print("Ex28 Check paths:", check_paths(BASE_URL, ["/", "/robots.txt"]))
    print("Ex29 Header:", get_header(BASE_URL, name="Server"))
    
    sec_headers = security_headers(BASE_URL)
    print("Ex30/31 Security score:", score_headers(sec_headers))
    
    robots_txt = fetch_robots(BASE_URL)
    print("Ex32 Disallowed paths:", disallowed_paths(robots_txt))
    
    print("Ex33 Times:", response_times(BASE_URL, "https://httpbin.org/get"))
    log("verificat", url=BASE_URL, status=200) # ex 34