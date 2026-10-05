import os
from PIL import Image

os.makedirs("probe", exist_ok=True)

# 1. probe/mesaj.txt (șir codat în straturi: Base64 -> Hex -> URL)
with open("probe/mesaj.txt", "w") as f:
    f.write("%255456d53545a686233567a5a5338")

# 2. probe/xor.bin (text criptat cu XOR pe un octet, cheia 0x5A)
mesaj_clar = b"Acesta este un mesaj secret XOR!"
cheie = 0x5A
mesaj_xor = bytes(b ^ cheie for b in mesaj_clar)
with open("probe/xor.bin", "wb") as f:
    f.write(mesaj_xor)

# 3. probe/hashuri.txt (hash MD5)
with open("probe/hashuri.txt", "w") as f:
    f.write("5f4dcc3b5aa765d61d8327deb882cf99") # hash-ul pentru "secret"

# 4. probe/wordlist.txt (pentru spargerea hash-ului)
with open("probe/wordlist.txt", "w") as f:
    f.write("parola\nadmin\nsecret\n123456\n")

# 5. probe/foto.jpg (o imagine simplă cu EXIF și GPS simulat)
img = Image.new('RGB', (200, 200), color = 'red')
img.save("probe/foto.jpg")

# 6. probe/ascuns.png (o poză cu o arhivă ZIP lipită la coadă - file carving)
img_png = Image.new('RGB', (100, 100), color = 'blue')
img_png.save("probe/ascuns.png")
with open("probe/ascuns.png", "ab") as f:
    f.write(b"PK\x03\x04" + b"\x00" * 20 + b"continut_arhiva_ascunsa")

print("Fișierele de probă au fost generate cu succes în folderul probe/!")