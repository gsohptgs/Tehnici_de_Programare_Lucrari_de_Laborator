# Raport Laboratorul 5 — Forensics și Steganografie

## Lucrarea A: Decoderul universal (`arsenal/forensics/decode.py`)

1. **Ce ascundea mesajul cu straturi (`probe/mesaj.txt`)**:
   - Straturi recunoscute și desfăcute: `base64 -> base64 -> hex`
   - Mesaj decodat: **`FLAG{straturi_de_encoding}`**

2. **Ce cheie XOR am găsit (`probe/xor.bin`)**:
   - Cheia XOR (1 octet): **`128`** (`0x80`)
   - Mesaj decriptat: **`Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`**

3. **Ce parole am spart din `probe/hashuri.txt` (algoritm MD5, lungime 32)**:
   - `5f4dcc3b5aa765d61d8327deb882cf99` -> **`password`**
   - `8621ffdbc5698829397d97767ac13db3` -> **`dragon`**
   - `d8578edf8458ce06fbc5bb76a58c5ca4` -> **`qwerty`**
   - `0d107d09f5bbe40cade3de5c71e9e9b7` -> **`letmein`**
   - `d0763edaa9d9bd2a9516280e9044d885` -> **`monkey`**

## Lucrarea B: Forensics pe fișiere și Steganografie LSB

1. **Tipul real al fișierelor (Magic Bytes)**:
   - `probe/foto.jpg`: **`jpeg`** (semnătura `\xff\xd8`)
   - `probe/ascuns.png`: **`png`** (semnătura `\x89PNG`)
   - `gasit.zip`: **`zip/docx`** (semnătura `PK\x03\x04`)

2. **Metadate EXIF și coordonate GPS (`probe/foto.jpg`)**:
   - Make: `Apple` | Model: `iPhone 13` | DateTime: `2026:09:14 10:30:00`
   - Coordonate GPS: **`47.016667 N, 28.8575 E`** (Chișinău, Republica Moldova)

3. **Arhiva ascunsă extrasă prin File Carving (`probe/ascuns.png`)**:
   - Arhiva `gasit.zip` a fost extrasă de la octetul `829`.
   - În interior se află `secret.txt` cu mesajul: **`FLAG{ascuns_prin_carving}`**

4. **Mesajul LSB ascuns și dezvăluit (`stego.png`)**:
   - Mesaj extras din ultimii biți ai pixelilor: **`FLAG{ascuns_in_pixeli}`**

## Bonus (`probe/challenge.bin`)
- Strat `base64` urmat de XOR cu cheia `128` (`0x80`) -> **`FLAG{lant_complet_despicat}`** (MD5: `8c4eb02d9dcef7d0ff91d8e4c7fea91b`).