// Service worker: offline support for Flashcards Dermatologie
const CACHE = 'derma-v1';
const SHELL = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Clinical images never change -> cache-first (offline once viewed)
  if (url.pathname.includes('/images/')) {
    e.respondWith(caches.open(CACHE).then(async c => {
      const hit = await c.match(req);
      if (hit) return hit;
      try { const res = await fetch(req); if (res.ok) c.put(req, res.clone()); return res; }
      catch (err) { return hit || Response.error(); }
    }));
    return;
  }

  // manifest.json is loaded with ?v=timestamp -> network-first (fresh data online),
  // fall back to cached copy offline (keyed without the query string)
  if (url.pathname.endsWith('manifest.json')) {
    const key = new Request(url.origin + url.pathname);
    e.respondWith(
      fetch(req).then(res => { caches.open(CACHE).then(c => c.put(key, res.clone())); return res; })
        .catch(() => caches.match(key))
    );
    return;
  }

  // App shell / everything else -> network-first, fall back to cache, then index.html
  e.respondWith(
    fetch(req).then(res => { caches.open(CACHE).then(c => c.put(req, res.clone())); return res; })
      .catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
  );
});
