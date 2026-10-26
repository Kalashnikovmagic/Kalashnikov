"""Собирает версию для GitHub Pages в папку docs/ (её раздаёт GitHub Pages) из kalashnikov.html."""
import json, os

from PIL import Image  # pip install pillow

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
os.makedirs(OUT, exist_ok=True)

HEAD = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<script>
// Запущено с экрана «Домой» как приложение — запрещаем зум (щипок, двойной тап, автозум полей).
if (matchMedia("(display-mode: standalone)").matches || navigator.standalone) {
  document.querySelector('meta[name=viewport]').setAttribute("content", "width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover");
  document.documentElement.style.touchAction = "pan-x pan-y";
  ["gesturestart", "gesturechange", "gestureend"].forEach(t => document.addEventListener(t, e => e.preventDefault(), {passive: false}));
  document.addEventListener("touchmove", e => { if (e.touches.length > 1) e.preventDefault() }, {passive: false});
  let lastTap = 0;
  document.addEventListener("touchend", e => { const now = Date.now(); if (now - lastTap < 300 && !e.target.closest("input,textarea,select")) e.preventDefault(); lastTap = now }, {passive: false});
}
</script>
<meta name="theme-color" content="#050505">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Kalashnikov">
<meta name="robots" content="noindex,nofollow">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-32.png?v=2" type="image/png">
<link rel="apple-touch-icon" href="icon-180.png?v=2">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
TAIL = """
<script>if("serviceWorker" in navigator && location.protocol==="https:") navigator.serviceWorker.register("sw.js");</script>
</body>
</html>
"""

src = open(os.path.join(ROOT, "kalashnikov.html"), encoding="utf8").read()
open(os.path.join(OUT, "index.html"), "w", encoding="utf8").write(HEAD + src + TAIL)

open(os.path.join(OUT, "sw.js"), "w", encoding="utf8").write("""const C="kalashnikov-v4";
const ASSETS=["./","./index.html","./manifest.webmanifest","./icon-192.png?v=2","./icon-512.png?v=2","./icon-180.png?v=2","./icon-32.png?v=2"];
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
    "name": "Kalashnikov", "short_name": "Kalashnikov", "lang": "ru",
    "start_url": "./", "scope": "./", "display": "standalone",
    "background_color": "#050505", "theme_color": "#050505",
    "icons": [{"src": "icon-192.png?v=2", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png?v=2", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
}, open(os.path.join(OUT, "manifest.webmanifest"), "w", encoding="utf8"), ensure_ascii=False, indent=1)


# Иконка: assets/icon-source.png (квадрат во весь размер, iOS сам скругляет углы).
master = Image.open(os.path.join(ROOT, "assets", "icon-source.png")).convert("RGB")
for s in (32, 180, 192, 512):
    master.resize((s, s), Image.LANCZOS).save(os.path.join(OUT, f"icon-{s}.png"), optimize=True)
open(os.path.join(OUT, ".nojekyll"), "w").close()
print("docs/ собран")
