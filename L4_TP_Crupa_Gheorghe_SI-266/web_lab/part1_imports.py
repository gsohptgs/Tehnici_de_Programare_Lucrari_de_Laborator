# Laborator: funcții, metode și importuri pe web
# Student: <Crupa Gheorghe>

import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 1
import requests
print("Versiune requests:", requests.__version__)
import urllib.request
# requests a avut nevoie de pip install deoarece este o bibliotecă externă. 
# urllib.request face parte din biblioteca standard Python și este deja preinstalată.

# Exercițiul 2
r1 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Stare requests.get:", r1.status_code)
from requests import get
r2 = get(BASE_URL, timeout=TIMEOUT)
print("Stare get:", r2.status_code)
# Avantaj `import requests`: Evită coliziunile de nume (știm exact din ce pachet vine funcția get).
# Avantaj `from requests import get`: Codul este mai scurt și mai ușor de scris.

# Exercițiul 3
import requests as rq
r3 = rq.get(BASE_URL, timeout=TIMEOUT)
# Un alias este ușor de citit când numele modulului original este foarte lung (ex. pandas as pd).
# Face codul mai greu de citit dacă alias-ul nu are sens sau dezvoltatorii nu sunt obișnuiți cu el.

# Exercițiul 4
response_urllib = urllib.request.urlopen(BASE_URL, timeout=TIMEOUT)
print("Stare urllib:", response_urllib.status)
corp_text = response_urllib.read().decode("utf-8")
print("Corp (200 carac.):", corp_text[:200])

# Exercițiul 5
print(dir(requests))
# 'get' este o funcție.
# 'Session' este o clasă.
# 'exceptions' este un modul.

# Exercițiul 6
# help(requests.get) -> arată parametrul timeout
r_timeout = requests.get(BASE_URL, timeout=TIMEOUT)

# Exercițiul 7
start = time.perf_counter()
r_perf = requests.get(BASE_URL, timeout=TIMEOUT)
end = time.perf_counter()
print("Timp perf_counter:", end - start)
print("Timp elapsed:", r_perf.elapsed.total_seconds())

# Exercițiul 8
try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")