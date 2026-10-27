import base64
import hashlib
import json
import re
from urllib.parse import unquote
import argparse

def ghici_strat(s):
    if "%" in s and re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s) and len(s) % 4 == 0:
        return "base64"
    return "necunoscut"

def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    elif strat == "hex":
        return strat, bytes.fromhex(s)
    elif strat == "url":
        return strat, unquote(s).encode()
    return "necunoscut", s.encode()

def citibil(b):
    return all(32 <= c < 127 for c in b)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare", nargs="?", default="")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.intrare:
        if a.fisier:
            with open(a.intrare, "rb") as f:
                val_bytes = f.read()
            val = val_bytes.decode(errors="ignore")
        else:
            val = a.intrare

        rezultat_final = val
        strat_final = "necunoscut"
        for _ in range(8):
            strat, b = desfa(rezultat_final if isinstance(rezultat_final, str) else rezultat_final.decode(errors="ignore"))
            if strat == "necunoscut":
                break
            rezultat_final = b
            strat_final = strat
            if citibil(b):
                break

        output_text = rezultat_final.decode(errors="ignore") if isinstance(rezultat_final, bytes) else rezultat_final
        
        fisa = {"strat": strat_final, "rezultat": output_text}
        with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
            json.dump(fisa, f, indent=4)
            
        print(f"Strat detectat: {strat_final}")
        print(f"Rezultat decodat: {output_text}")