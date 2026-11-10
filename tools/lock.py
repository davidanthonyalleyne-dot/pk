#!/usr/bin/env python3
"""Encrypt the PK game page into game.bin so the public repo holds nothing playable.

Usage: python3 tools/lock.py path/to/pk.html ABCD-EFGH-JKLM-NPQR

The page in index.html asks for the same code, derives the key in the browser
and decrypts game.bin. Changing the code means running this again and committing
the new game.bin; old invite links then stop working.
"""
import gzip, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 250000
ALPHA = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

src, code = sys.argv[1], sys.argv[2]
code = "".join(ch for ch in code.upper() if ch.isalnum())
assert len(code) == 16 and all(ch in ALPHA for ch in code), "code must be 16 letters and numbers"

html = open(src, encoding="utf-8").read()
head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="theme-color" content="#15161a">'
        '<link rel="manifest" href="manifest.webmanifest">'
        '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">'
        '<script>window.__noGate=1</script>')
tail = ('<script>(function(){var a=document.querySelector("#sheet .acts");if(!a)return;'
        'var b=document.createElement("button");b.className="btn ghost";b.type="button";'
        'b.textContent="Lock this device";b.onclick=function(){try{localStorage.removeItem("pkCode")}catch(e){}'
        'location.replace(location.pathname)};a.appendChild(b)})();</script>')
html = html.replace("</body></html>", tail + "</body></html>") if "</body></html>" in html else html + tail
data = gzip.compress((head + html).encode("utf-8"), 9)

salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(code.encode())
out = b"PK1" + salt + iv + AESGCM(key).encrypt(iv, data, None)
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "game.bin")
open(dst, "wb").write(out)
print(f"wrote game.bin, {len(out)//1024} KB")
