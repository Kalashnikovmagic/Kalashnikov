const C="kalashnikov-1794160976";
const ASSETS=["./","./index.html","./manifest.webmanifest","./icon-192.png?v=2","./icon-512.png?v=2","./icon-180.png?v=2","./icon-32.png?v=2"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(ASSETS)));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
// Сначала сеть (страницу и номер версии — мимо кэша браузера, чтобы обновления приходили сразу), без сети — из кэша.
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET") return; const fresh=e.request.mode==="navigate"||/(index\.html|version\.txt)$/.test(new URL(e.request.url).pathname);
  e.respondWith(fetch(e.request,fresh?{cache:"no-store"}:{}).then(r=>{const cp=r.clone(); if(r.ok) caches.open(C).then(c=>c.put(e.request,cp)); return r})
    .catch(()=>caches.match(e.request).then(r=>r||caches.match("./index.html"))));
});
