# Laborator: funcții, metode și importuri pe web
# Student: <Crupa Gheorghe>

import urllib.parse
import re
import hashlib
import json
import socket
import ssl
from datetime import datetime
import requests
from html.parser import HTMLParser

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# Exercițiul 35
def url_breakdown(url):
    p = urllib.parse.urlparse(url)
    print(f"Scheme: {p.scheme}, Netloc: {p.netloc}, Path: {p.path}, Query: {p.query}, Fragment: {p.fragment}")

# Exercițiul 36
def build_urls(base, paths):
    for p in paths:
        print("Mergând din", base, ":", urllib.parse.urljoin(base, p))

# Exercițiul 37
def extract_links(html):
    links = re.findall(r'href="([^"]+)"', html)
    return list(set(links)) # elimină duplicatele

# Exercițiul 38
def split_links(links, domain):
    internale, externe = [], []
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        if urllib.parse.urlparse(full_url).netloc == domain:
            internale.append(full_url)
        else:
            externe.append(full_url)
    return internale, externe

# Exercițiul 39
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

# Exercițiul 40
def page_fingerprint(url):
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()

# Exercițiul 41
def save_and_load_json(url):
    response = requests.get(url, timeout=TIMEOUT)
    with open("headers.json", "w") as file:
        json.dump(dict(response.headers), file, indent=2)
    with open("headers.json", "r") as file:
        loaded = json.load(file)
        print("Din JSON, Content-Type:", loaded.get("Content-Type"))

# Exercițiul 42
def resolve(hostname):
    return socket.gethostbyname(hostname)

# Exercițiul 43
def cert_days_left(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_after = cert["notAfter"]
            expire_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            days_left = (expire_date - datetime.utcnow()).days
            return days_left

if __name__ == "__main__":
    url_breakdown("https://cybercor.org/path?x=1#top")
    build_urls(BASE_URL, ["/about", "contact.html", "../index.html"])
    
    html = requests.get(BASE_URL, timeout=TIMEOUT).text
    links = extract_links(html)
    internale, externe = split_links(links, "cybercor.org")
    print(f"Lnk interne: {len(internale)}, Lnk externe: {len(externe)}")
    
    test_html = """<html><body>
      <img src="/logo.png" alt="Logo">
      <IMG SRC="poza.jpg">
      <img alt="imagine fără src">
      <img src="https://cdn.example.com/banner.webp" />
      <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>"""
    finder = ImageFinder()
    finder.feed(test_html)
    assert finder.images == ["/logo.png", "poza.jpg", "https://cdn.example.com/banner.webp"], "Eroare parser"
    
    fp1 = page_fingerprint(BASE_URL)
    fp2 = page_fingerprint(BASE_URL)
    print("Fingerprints match:", fp1 == fp2)
    # Răspuns: Când site-ul se modifică sau adaugă elemente dinamice (timpi randare, token-uri csrf), hash-ul diferă.

    save_and_load_json(BASE_URL)
    print("IP cybercor:", resolve("cybercor.org"))
    print("Zile certificat:", cert_days_left("cybercor.org"))