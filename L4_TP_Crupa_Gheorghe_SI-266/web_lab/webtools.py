# Laborator: funcții, metode și importuri pe web
# Student: <Crupa Gheorghe>

import requests
import urllib.parse
import json
import socket
import time

TIMEOUT = 10
# Exercițiul 47
DEFAULT_HEADERS = {"User-Agent": "WebLab-Crupa-Gheorghe"}

def fetch(url, timeout=TIMEOUT):
    return requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)

def get_status(url: str) -> int:
    return fetch(url).status_code

def get_title(html):
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return None

def security_headers(url):
    response = fetch(url)
    headers_to_check = [
        "Strict-Transport-Security", "Content-Security-Policy",
        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"
    ]
    return {h: h in response.headers for h in headers_to_check}

def score_headers(results):
    score = sum(1 for val in results.values() if val)
    return f"{score}/{len(results)}"

# --- Funcții aduse din part 3/4 pentru raport ---
def fetch_robots(base):
    try:
        r = fetch(base.rstrip("/") + "/robots.txt")
        return r.text if r.status_code == 200 else None
    except:
        return None

def disallowed_paths(robots_text):
    if not robots_text: return []
    return [line.split(":", 1)[1].strip() for line in robots_text.splitlines() if line.startswith("Disallow:")]

import re
def extract_links(html):
    return list(set(re.findall(r'href="([^"]+)"', html)))

def split_links(links, domain):
    internale, externe = [], []
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        if urllib.parse.urlparse(full_url).netloc == domain:
            internale.append(full_url)
        else:
            externe.append(full_url)
    return internale, externe

import ssl
from datetime import datetime
def cert_days_left(hostname):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after = cert["notAfter"]
                expire_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                return (expire_date - datetime.utcnow()).days
    except Exception:
        return "Eroare certificat"

def resolve(hostname):
    try:
        return socket.gethostbyname(hostname)
    except:
        return "IP necunoscut"

# Exercițiul 50
def site_report(url):
    print(f"=== Raport site: {url} ===")
    
    # Detalii rețea
    response = fetch(url)
    status = response.status_code
    html = response.text
    domain = urllib.parse.urlparse(url).netloc
    ip = resolve(domain)
    
    # Redirecționări
    r_http = requests.get(url.replace("https://", "http://"), timeout=TIMEOUT)
    redirections = " -> ".join([str(r.status_code) for r in r_http.history] + [r_http.url]) if r_http.history else r_http.url

    # Elemente pagină
    title = get_title(html)
    sec_score = score_headers(security_headers(url))
    cert_days = cert_days_left(domain)
    
    # Legături
    links = extract_links(html)
    internale, externe = split_links(links, domain)
    
    # Robots.txt
    robots_txt = fetch_robots(url)
    disallowed = disallowed_paths(robots_txt)
    
    # Generare dicționar pt JSON
    report_data = {
        "url": url,
        "status": status,
        "titlu": title,
        "ip": ip,
        "redirectionari": redirections,
        "scor_securitate": sec_score,
        "certificat_zile": cert_days,
        "linkuri_interne": len(internale),
        "linkuri_externe": len(externe),
        "cai_interzise": disallowed
    }
    
    # Output pe ecran
    print(f"Cod de stare:      {status}")
    print(f"Titlu:             {title}")
    print(f"Adresă IP:         {ip}")
    print(f"Redirecționări:    {redirections}")
    print(f"Scor securitate:   {sec_score}")
    print(f"Certificat:        {cert_days} de zile rămase")
    print(f"Legături:          {len(internale)} interne, {len(externe)} externe")
    print(f"Căi interzise:     {', '.join(disallowed) if disallowed else 'Niciuna'}")
    
    with open("report.json", "w") as f:
        json.dump(report_data, f, indent=4)
    print("Salvat în report.json")

# Exercițiul 46
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
    # Autotestul rulează doar aici pentru că fișierul e executat ca script principal (__main__). 
    # Când îl importăm din main.py, variabila magică __name__ devine "webtools", deci nu se rulează.