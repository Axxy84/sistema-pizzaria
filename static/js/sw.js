// Service Worker para Cache Offline
const CACHE_NAME = 'pizzaria-v1';
const urlsToCache = [
    '/',
    '/static/css/base.css',
    '/static/css/pedidos.css',
    '/static/js/base-optimized.js',
    '/static/images/logo.svg',
    // Alpine.js e Tailwind do CDN
    'https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js',
    'https://cdn.tailwindcss.com'
];

// Instalar Service Worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Cache aberto');
                return cache.addAll(urlsToCache);
            })
    );
});

// Ativar Service Worker
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];
    
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Estratégia de Cache: Network First, Cache Fallback
self.addEventListener('fetch', event => {
    // Ignorar requisições não-GET
    if (event.request.method !== 'GET') {
        return;
    }
    
    // Para API, sempre tentar rede primeiro
    if (event.request.url.includes('/api/')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    // Clonar a resposta
                    const responseToCache = response.clone();
                    
                    caches.open(CACHE_NAME)
                        .then(cache => {
                            cache.put(event.request, responseToCache);
                        });
                    
                    return response;
                })
                .catch(() => {
                    // Se falhar, tentar cache
                    return caches.match(event.request);
                })
        );
        return;
    }
    
    // Para assets estáticos, cache first
    if (event.request.url.includes('/static/') || 
        event.request.url.includes('cdn.jsdelivr.net') ||
        event.request.url.includes('fonts.googleapis.com')) {
        
        event.respondWith(
            caches.match(event.request)
                .then(response => {
                    if (response) {
                        return response;
                    }
                    
                    return fetch(event.request).then(response => {
                        // Não cachear respostas com erro
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        
                        const responseToCache = response.clone();
                        
                        caches.open(CACHE_NAME)
                            .then(cache => {
                                cache.put(event.request, responseToCache);
                            });
                        
                        return response;
                    });
                })
        );
        return;
    }
    
    // Para outras requisições, network first
    event.respondWith(
        fetch(event.request)
            .catch(() => {
                return caches.match(event.request);
            })
    );
});