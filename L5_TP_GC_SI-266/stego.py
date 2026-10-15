# -*- coding: utf-8 -*-
from PIL import Image

# B5. Ascunzi un mesaj prin LSB
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}\x00"
biti = "".join(f"{x:08b}" for x in mesaj)

it_biti = iter(biti)
px_nou = []
for (r, g, b) in px:
    canale = [r, g, b]
    for i in range(3):
        bit = next(it_biti, None)
        if bit is not None:
            canale[i] = (canale[i] & ~1) | int(bit)
    px_nou.append(tuple(canale))

img.putdata(px_nou)
img.save("stego.png")
print("Mesaj ascuns salvat in stego.png")

# B6. Dezvalui mesajul inapoi
px_stego = list(Image.open("stego.png").convert("RGB").getdata())
biti_extrasi = ""
for (r, g, b) in px_stego:
    biti_extrasi += f"{r & 1}{g & 1}{b & 1}"

octeti = bytearray()
for i in range(0, len(biti_extrasi) - 7, 8):
    octet = int(biti_extrasi[i:i+8], 2)
    if octet == 0:
        break
    octeti.append(octet)

print("Mesaj dezvaluit:", octeti.decode("utf-8", errors="replace"))