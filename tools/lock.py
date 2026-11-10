#!/usr/bin/env python3
"""Encrypt the PK game page into game.bin so the public repo holds nothing playable.

Usage: python3 tools/lock.py path/to/pk.html ABCD-EFGH-JKLM-NPQR

The page in index.html asks for the same code, derives the key in the browser
and decrypts game.bin. Changing the code means running this again and committing
the new game.bin; old invite links then stop working.
"""
import gzip, hashlib, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 250000
ALPHA = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

src, code = sys.argv[1], sys.argv[2]
code = "".join(ch for ch in code.upper() if ch.isalnum())
assert len(code) == 16 and all(ch in ALPHA for ch in code), "code must be 16 letters and numbers"

html = open(src, encoding="utf-8").read()
ver = hashlib.sha256(html.encode("utf-8")).hexdigest()[:12]
head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="theme-color" content="#15161a">'
        '<link rel="manifest" href="manifest.webmanifest">'
        '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">'
        '<script>window.__noGate=1;window.__PKV="' + ver + '"</script>')
tail = ('<script>(function(){var a=document.querySelector("#sheet .acts");if(!a)return;'
        'var b=document.createElement("button");b.className="btn ghost";b.type="button";'
        'b.textContent="Lock this device";b.onclick=function(){try{localStorage.removeItem("pkCode")}catch(e){}'
        'location.replace(location.pathname)};a.appendChild(b)})();</script>')
# check for a newer PK whenever the app comes back to the front, and every few minutes while playing
upd = ('<script>(function(){var busy=false,shown=false;'
       'function bar(){if(shown)return;shown=true;var b=document.createElement("button");b.type="button";'
       'b.textContent="PK was updated. Tap to load it";b.style.cssText="position:fixed;left:50%;transform:translateX(-50%);'
       'bottom:calc(env(safe-area-inset-bottom,0px) + 18px);z-index:60;border:0;border-radius:22px;padding:12px 18px;'
       'font:600 15px/1 Barlow,system-ui,sans-serif;background:#f3b23c;color:#1a1408;box-shadow:0 6px 18px rgba(0,0,0,.4)";'
       'b.onclick=function(){location.reload()};document.body.appendChild(b)}'
       'function check(back){if(busy||!window.__PKV)return;busy=true;fetch("version.json?t="+Date.now(),{cache:"no-store"})'
       '.then(function(r){return r.ok?r.json():null}).then(function(j){busy=false;if(!j||!j.v||j.v===window.__PKV)return;'
       'var t=document.getElementById("title");if(t&&!t.hidden)location.reload();else bar()}).catch(function(){busy=false})}'
       'document.addEventListener("visibilitychange",function(){if(document.visibilityState==="visible")check(true)});'
       'window.addEventListener("pageshow",function(e){if(e.persisted)check(true)});'
       'setInterval(function(){if(document.visibilityState==="visible")check(false)},300000);setTimeout(function(){check(false)},4000)})();</script>')
tail = tail + upd
html = html.replace("</body></html>", tail + "</body></html>") if "</body></html>" in html else html + tail
data = gzip.compress((head + html).encode("utf-8"), 9)

salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(code.encode())
out = b"PK1" + salt + iv + AESGCM(key).encrypt(iv, data, None)
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "game.bin")
open(dst, "wb").write(out)
json.dump({"v": ver}, open(os.path.join(os.path.dirname(dst), "version.json"), "w"))
print(f"wrote game.bin, {len(out)//1024} KB, version {ver}")
