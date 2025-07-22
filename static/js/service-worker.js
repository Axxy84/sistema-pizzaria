// Service Worker para PWA - Sistema de Gestão Pizzaria
const CACHE_NAME = 'pizzaria-v1.0.0';
const urlsToCache = [
  '/',
  '/static/css/base.css',
  '/static/js/base-optimized.js',
  '/static/images/logo.svg',
  '/offline.html'
];

// Instalação do Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache aberto');
        return cache.addAll(urlsToCache);
      })
  );
  // Força ativação imediata
  self.skipWaiting();
});

// Ativação e limpeza de caches antigos
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Removendo cache antigo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  // Assume controle imediato
  self.clients.claim();
});

// Estratégia de cache: Network First com fallback
self.addEventListener('fetch', event => {
  // Ignorar requisições não-GET
  if (event.request.method !== 'GET') {
    return;
  }

  // Estratégia para API: sempre rede
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request)
        .catch(() => {
          return new Response(
            JSON.stringify({ error: 'Sem conexão com servidor' }),
            { headers: { 'Content-Type': 'application/json' } }
          );
        })
    );
    return;
  }

  // Estratégia para assets estáticos: cache first
  if (event.request.url.includes('/static/')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          if (response) {
            return response;
          }
          return fetch(event.request).then(response => {
            // Adiciona ao cache se for sucesso
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

  // Estratégia padrão: Network first com cache fallback
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Cache de páginas HTML bem-sucedidas
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }
        const responseToCache = response.clone();
        caches.open(CACHE_NAME)
          .then(cache => {
            cache.put(event.request, responseToCache);
          });
        return response;
      })
      .catch(() => {
        // Tenta cache, senão mostra página offline
        return caches.match(event.request)
          .then(response => {
            if (response) {
              return response;
            }
            // Se for navegação, mostra página offline
            if (event.request.mode === 'navigate') {
              return caches.match('/offline.html');
            }
          });
      })
  );
});

// Sincronização em background
self.addEventListener('sync', event => {
  if (event.tag === 'sync-pedidos') {
    event.waitUntil(syncPedidosOffline());
  }
});

// Push notifications
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'Novo pedido recebido!',
    icon: '/static/images/icon-192x192.png',
    badge: '/static/images/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'view',
        title: 'Ver pedido',
        icon: '/static/images/icon-view.png'
      },
      {
        action: 'close',
        title: 'Fechar',
        icon: '/static/images/icon-close.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Pizzaria - Novo Pedido', options)
  );
});

// Clique em notificações
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'view') {
    event.waitUntil(
      clients.openWindow('/pedidos/novos/')
    );
  }
});

// Função auxiliar para sincronizar pedidos offline
async function syncPedidosOffline() {
  try {
    // Busca pedidos pendentes no IndexedDB
    const pedidosPendentes = await getPedidosPendentes();
    
    for (const pedido of pedidosPendentes) {
      try {
        const response = await fetch('/api/pedidos/criar/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(pedido)
        });
        
        if (response.ok) {
          await removePedidoPendente(pedido.id);
        }
      } catch (error) {
        console.error('Erro ao sincronizar pedido:', error);
      }
    }
  } catch (error) {
    console.error('Erro na sincronização:', error);
  }
}

// Placeholder para funções IndexedDB
async function getPedidosPendentes() {
  // Implementar busca no IndexedDB
  return [];
}

async function removePedidoPendente(id) {
  // Implementar remoção do IndexedDB
}