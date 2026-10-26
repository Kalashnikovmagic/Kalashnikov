"""Собирает версию для GitHub Pages в папку docs/ (её раздаёт GitHub Pages) из zhelezo.html."""
import json, os, struct, zlib

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
os.makedirs(OUT, exist_ok=True)

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#1F4FD8">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Железо">
<meta name="robots" content="noindex,nofollow">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="icon-180.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
TAIL = """
<script>if("serviceWorker" in navigator && location.protocol==="https:") navigator.serviceWorker.register("sw.js");</script>
</body>
</html>
"""

src = open(os.path.join(ROOT, "zhelezo.html"), encoding="utf8").read()
open(os.path.join(OUT, "index.html"), "w", encoding="utf8").write(HEAD + src + TAIL)

open(os.path.join(OUT, "sw.js"), "w", encoding="utf8").write("""const C="zhelezo-v1";
const ASSETS=["./","./index.html","./manifest.webmanifest","./icon-192.png","./icon-512.png","./icon-180.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(ASSETS)));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
// Сначала сеть (чтобы обновления приходили сразу), без сети — из кэша.
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET") return;
  e.respondWith(fetch(e.request).then(r=>{const cp=r.clone(); if(r.ok) caches.open(C).then(c=>c.put(e.request,cp)); return r})
    .catch(()=>caches.match(e.request).then(r=>r||caches.match("./index.html"))));
});
""")

json.dump({
    "name": "Железо и дела", "short_name": "Железо", "lang": "ru",
    "start_url": "./", "scope": "./", "display": "standalone",
    "background_color": "#ECEFF3", "theme_color": "#1F4FD8",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
}, open(os.path.join(OUT, "manifest.webmanifest"), "w", encoding="utf8"), ensure_ascii=False, indent=1)


def icon(size):
    """Синий фон и белая штанга: гриф и по два блина с каждой стороны."""
    bg, fg = (0x1F, 0x4F, 0xD8), (0xFF, 0xFF, 0xFF)
    u = size / 32
    rects = [(4, 15, 28, 17),            # гриф
             (6, 9, 8, 23), (9, 11, 11, 21),   # блины слева
             (24, 9, 26, 23), (21, 11, 23, 21)]  # блины справа
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            on = any(a * u <= x < c * u and b * u <= y < d * u for a, b, c, d in rects)
            row += bytes(fg if on else bg)
        rows.append(bytes(row))
    raw = zlib.compress(b"".join(rows), 9)
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)) + chunk(b"IDAT", raw) + chunk(b"IEND", b"")


for s in (180, 192, 512):
    open(os.path.join(OUT, f"icon-{s}.png"), "wb").write(icon(s))
open(os.path.join(OUT, ".nojekyll"), "w").close()
print("docs/ собран")
