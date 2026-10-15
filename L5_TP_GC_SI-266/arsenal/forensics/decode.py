# -*- coding: utf-8 -*-
import os
import re
import json
import base64
import hashlib
import argparse
from urllib.parse import unquote

# A1. Text si octeti: incalzirea
s = "Salut"
b = s.encode()
print(b, b[0], b.hex(), bytes.fromhex(b.hex()))

# A2. Recunosti stratul dupa forma
def ghici_strat(s):
    if not isinstance(s, str):
        try:
            s = s.decode("ascii")
        except UnicodeDecodeError:
            return "necunoscut"
    s = s.strip()
    if not s:
        return "necunoscut"
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"
    if len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"

# A3. Desfaci stratul recunoscut
def desfa(s):
    if isinstance(s, bytes):
        s = s.decode("ascii", errors="ignore")
    s = s.strip()
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    if strat == "hex":
        return strat, bytes.fromhex(s)
    if strat == "url":
        return strat, unquote(s).encode("utf-8")
    return strat, s.encode("utf-8")

# A4. Straturi multiple, intr-o bucla
def citibil(b):
    return len(b) > 0 and all(32 <= c < 127 or c in (9, 10, 13) for c in b)

def desfa_straturi(val):
    straturi = []
    b = val.encode() if isinstance(val, str) else val
    for _ in range(8):
        strat, b_nou = desfa(val)
        if strat == "necunoscut":
            break
        straturi.append(strat)
        b = b_nou
        if citibil(b):
            text = b.decode("ascii").strip()
            urm_strat, urm_b = desfa(text)
            if urm_strat == "necunoscut" or not citibil(urm_b):
                break
            val = text
        else:
            break
    return straturi, b

if __name__ == "__main__":
    # A5. Spargi un XOR cu cheie de un octet
    if os.path.exists("probe/xor.bin"):
        date = open("probe/xor.bin", "rb").read()
        for k in range(256):
            clar = bytes(x ^ k for x in date)
            if citibil(clar):
                print("cheie:", k, clar.decode())

    # A6. Spargi un hash prin dictionar
    if os.path.exists("probe/hashuri.txt") and os.path.exists("probe/wordlist.txt"):
        for linie in open("probe/hashuri.txt"):
            tinta = linie.strip()
            if not tinta:
                continue
            for cuv in open("probe/wordlist.txt", encoding="latin1"):
                cuv = cuv.strip()
                if hashlib.md5(cuv.encode()).hexdigest() == tinta:
                    print("gasit:", cuv)
                    break

    # A7. argparse si fisa JSON
    p = argparse.ArgumentParser()
    p.add_argument("intrare", nargs="?", default="probe/mesaj.txt")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier or os.path.exists(a.intrare):
        continut = open(a.intrare, "r", encoding="utf-8").read().strip()
    else:
        continut = a.intrare

    straturi, rez = desfa_straturi(continut)
    fisa = {
        "strat": " -> ".join(straturi) if straturi else ghici_strat(continut),
        "rezultat": rez.decode("utf-8", errors="replace")
    }
    os.makedirs("arsenal/forensics", exist_ok=True)
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=2, ensure_ascii=False)
    print("Fisa salvata:", fisa)