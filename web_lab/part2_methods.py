# Laborator: funcții, metode și importuri pe web
# Student: <Crupa Gheorghe>

import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 9
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Status code:", response.status_code)  # atribut
print("OK:", response.ok)                    # atribut
print("URL:", response.url)                  # atribut
print("Encoding:", response.encoding)        # atribut

# Exercițiul 10
response.raise_for_status()
try:
    time.sleep(1)
    r_bad = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    r_bad.raise_for_status()
except requests.HTTPError:
    print("Pagina nu există! (Eroare prinsă elegant)")

# Exercițiul 11
print("Antete:")
for name, value in response.headers.items():
    print(f"{name}: {value}")

# Exercițiul 12
print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type mic:", response.headers.get("content-type", "lipsește"))
# Ce observați: Dicționarul de antete din requests ignoră majusculele/minusculele (CaseInsensitiveDict).

# Exercițiul 13
print("Cuvântul cyber apare de:", response.text.lower().count("cyber"), "ori")
# Puteți înlănțui .lower() și .count() deoarece .lower() returnează un string, iar clasa string are metoda .count().

# Exercițiul 14
html = response.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>")
titlu = html[start:end].strip() if start != -1 and end != -1 else "Fără titlu"
print("Titlu manual:", titlu)

# Exercițiul 15
lines = html.splitlines()
print("Număr linii HTML:", len(lines))
print("Cea mai lungă linie are:", len(max(lines, key=len)), "caractere")

# Exercițiul 16
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

# Exercițiul 17
time.sleep(1)
r_http = requests.get("http://cybercor.org", timeout=TIMEOUT)
for resp in r_http.history:
    print("Redirecționare:", resp.status_code, resp.url)
print("URL final:", r_http.url)

# Exercițiul 18
time.sleep(1)
r_head = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
r_get = requests.get(BASE_URL, timeout=TIMEOUT)
print("Lungime content HEAD:", len(r_head.content))
print("Lungime content GET:", len(r_get.content))
# HEAD cere doar antetele, fără a descărca efectiv corpul, pe când GET descarcă toată pagina.

# Exercițiul 19
if not r_get.cookies:
    print("Niciun cookie setat")
else:
    for cookie in r_get.cookies:
        print("Cookie:", cookie.name, "Secure:", cookie.secure)

# Exercițiul 20
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-<numele vostru>"})
time.sleep(1)
r_sess = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Sesiune - Răspuns headers:", r_sess.json())