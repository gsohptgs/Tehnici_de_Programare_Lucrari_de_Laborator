# Laborator: funcții, metode și importuri pe web
# Student: <Crupa Gheorghe>

# Ex 45: Din ce în ce importăm mai specific
from webtools import get_status, get_title, fetch, site_report, DEFAULT_HEADERS
import argparse
import csv
from datetime import datetime
import time

# Dacă main.py ar avea o funcție proprie `get_title`, aceasta ar suprascrie (sau ar fi suprascrisă)
# de funcția importată, creând conflicte. De aceea, structurile sigure sunt `import webtools`.

def generate_csv_report(url):
    paths_to_check = ["/", "/robots.txt", "/sitemap.xml", "/non-existent"]
    results = []
    
    for path in paths_to_check:
        full_url = url.rstrip("/") + path
        try:
            status = get_status(full_url)
        except:
            status = "Eroare"
        results.append({
            "path": path,
            "status": status,
            "checked_at": datetime.now().isoformat()
        })
        time.sleep(1)
        
    with open("report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "status", "checked_at"])
        writer.writeheader()
        writer.writerows(results)
    print("\n[+] Raportul CSV pentru rute a fost creat.")

# Ex 48
def main():
    parser = argparse.ArgumentParser(description="WebLab Reporter")
    parser.add_argument("url", nargs="?", default="https://cybercor.org", help="URL-ul țintă")
    args = parser.parse_args()

    print("Header default:", DEFAULT_HEADERS) # ex 47
    
    # Ex 49
    generate_csv_report(args.url)
    
    # Ex 50
    print("\nGenerare raport site final...")
    site_report(args.url)

if __name__ == "__main__":
    main()