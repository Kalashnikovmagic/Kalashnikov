const C="kalashnikov-v2";
const ASSETS=["./","./index.html","./manifest.webmanifest","./icon-192.png","./icon-512.png","./icon-180.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(ASSETS)));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
// Сначала сеть (чтобы обновления приходили сразу), без сети — из кэша.
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET") return;
  e.respondWith(fetch(e.request).then(r=>{const cp=r.clone(); if(r.ok) caches.open(C).then(c=>c.put(e.request,cp)); return r})
    .catch(()=>caches.match(e.request).then(r=>r||caches.match("./index.html"))));
});
