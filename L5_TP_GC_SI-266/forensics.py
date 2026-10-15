# -*- coding: utf-8 -*-
import re
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# B1. Magic bytes: tipul real, nu extensia
def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()

def dms_la_zecimal(dms, ref):
    z = float(dms[0]) + (float(dms[1]) / 60.0) + (float(dms[2]) / 3600.0)
    return round(-z if ref in ("S", "W") else z, 6)

if __name__ == "__main__":
    # B1. Magic bytes
    print("foto.jpg ->", tip_real("probe/foto.jpg"))
    print("ascuns.png ->", tip_real("probe/ascuns.png"))

    # B2. strings: textul citibil dintr-un binar
    date = open("probe/ascuns.png", "rb").read()
    for m in re.findall(rb"[ -~]{4,}", date):
        print(m.decode("ascii", errors="ignore"))

    # B3. Metadate EXIF si GPS din poza
    exif = Image.open("probe/foto.jpg")._getexif() or {}
    for id, val in exif.items():
        print(TAGS.get(id, id), "=", val)
        if id == 34853:
            gps = {GPSTAGS.get(k, k): v for k, v in val.items()}
            lat = dms_la_zecimal(gps["GPSLatitude"], gps["GPSLatitudeRef"])
            lon = dms_la_zecimal(gps["GPSLongitude"], gps["GPSLongitudeRef"])
            print(f"Coordonate GPS zecimale: {lat} N, {lon} E")

    # B4. File carving: scoti fisierul ascuns
    i = date.find(b"PK\x03\x04")
    if i != -1:
        open("gasit.zip", "wb").write(date[i:])
        print("arhiva extrasa de la octetul", i)
        with zipfile.ZipFile("gasit.zip", "r") as z:
            print("Continut secret.txt:", z.read("secret.txt").decode().strip())