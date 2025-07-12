// Base JavaScript Otimizado - Módulos e Lazy Loading
(() => {
    'use strict';
    
    // Utilitários otimizados
    const PizzariaUtils = {
        // Cache de elementos DOM
        elementCache: new Map(),
        
        // Obter elemento com cache
        getElement(selector) {
            if (!this.elementCache.has(selector)) {
                this.elementCache.set(selector, document.querySelector(selector));
            }
            return this.elementCache.get(selector);
        },
        
        // Formatar moeda brasileiro
        formatCurrency(value) {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(value);
        },
        
        // Formatar data
        formatDate(date) {
            return new Intl.DateTimeFormat('pt-BR').format(new Date(date));
        },
        
        // Obter cookie CSRF
        getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        },
        
        // Debounce otimizado
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        // Throttle otimizado
        throttle(func, limit) {
            let inThrottle;
            return function(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }
    };
    
    // Expor globalmente
    window.PizzariaUtils = PizzariaUtils;
    
    // Inicialização Alpine.js otimizada
    document.addEventListener('alpine:init', () => {
        
        // Store Global Otimizado
        Alpine.store('app', {
            loading: false,
            toastQueue: [],
            
            setLoading(state) {
                this.loading = state;
                // Usar requestAnimationFrame para melhor performance
                requestAnimationFrame(() => {
                    const loader = PizzariaUtils.getElement('.global-loader');
                    if (loader) {
                        loader.style.display = state ? 'flex' : 'none';
                    }
                });
            },
            
            showToast(message, type = 'info', duration = 5000) {
                // Limitar fila de toasts
                if (this.toastQueue.length > 5) {
                    this.toastQueue.shift();
                }
                
                this.toastQueue.push({ message, type, duration });
                window.dispatchEvent(new CustomEvent('show-toast', {
                    detail: { message, type, duration }
                }));
            },
            
            showAlert(message, type = 'info') {
                const event = new CustomEvent('show-alert', {
                    detail: { message, type }
                });
                window.dispatchEvent(event);
            }
        });
        
        // Modal Component Otimizado
        Alpine.data('modal', (initialOpen = false) => ({
            open: initialOpen,
            scrollPosition: 0,
            
            show() {
                this.scrollPosition = window.scrollY;
                this.open = true;
                document.body.style.overflow = 'hidden';
                document.body.style.position = 'fixed';
                document.body.style.top = `-${this.scrollPosition}px`;
                document.body.style.width = '100%';
            },
            
            hide() {
                this.open = false;
                document.body.style.overflow = '';
                document.body.style.position = '';
                document.body.style.top = '';
                document.body.style.width = '';
                window.scrollTo(0, this.scrollPosition);
            },
            
            toggle() {
                this.open ? this.hide() : this.show();
            }
        }));
        
        // Form Component Otimizado
        Alpine.data('form', (options = {}) => ({
            loading: false,
            errors: {},
            
            async submit(formData) {
                this.loading = true;
                this.errors = {};
                
                try {
                    const response = await fetch(options.url, {
                        method: options.method || 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': PizzariaUtils.getCookie('csrftoken')
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        Alpine.store('app').showToast(
                            data.message || 'Operação realizada com sucesso!',
                            'success'
                        );
                        
                        if (options.onSuccess) {
                            options.onSuccess(data);
                        }
                        
                        if (data.redirect) {
                            setTimeout(() => {
                                window.location.href = data.redirect;
                            }, 1000);
                        }
                    } else {
                        this.errors = data.errors || {};
                        Alpine.store('app').showToast(
                            data.message || 'Erro ao processar solicitação',
                            'error'
                        );
                    }
                } catch (error) {
                    console.error('Form error:', error);
                    Alpine.store('app').showToast(
                        'Erro de conexão. Tente novamente.',
                        'error'
                    );
                } finally {
                    this.loading = false;
                }
            },
            
            hasError(field) {
                return this.errors.hasOwnProperty(field);
            },
            
            getError(field) {
                return this.errors[field]?.[0] || '';
            }
        }));
        
        // Table Component Otimizado
        Alpine.data('table', (options = {}) => ({
            data: [],
            loading: false,
            page: 1,
            perPage: options.perPage || 20,
            total: 0,
            search: '',
            orderBy: options.orderBy || 'id',
            orderDir: 'asc',
            
            async loadData() {
                this.loading = true;
                
                const params = new URLSearchParams({
                    page: this.page,
                    limit: this.perPage,
                    search: this.search,
                    order_by: this.orderBy,
                    order_dir: this.orderDir
                });
                
                try {
                    const response = await fetch(`${options.url}?${params}`);
                    const result = await response.json();
                    
                    this.data = result.data || [];
                    this.total = result.total || 0;
                } catch (error) {
                    console.error('Table error:', error);
                    Alpine.store('app').showToast('Erro ao carregar dados', 'error');
                } finally {
                    this.loading = false;
                }
            },
            
            // Busca com debounce
            searchDebounced: PizzariaUtils.debounce(function() {
                this.page = 1;
                this.loadData();
            }, 300),
            
            sort(field) {
                if (this.orderBy === field) {
                    this.orderDir = this.orderDir === 'asc' ? 'desc' : 'asc';
                } else {
                    this.orderBy = field;
                    this.orderDir = 'asc';
                }
                this.loadData();
            },
            
            changePage(newPage) {
                this.page = newPage;
                this.loadData();
            },
            
            init() {
                this.loadData();
            }
        }));
    });
    
    // Lazy Loading de Imagens
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        document.addEventListener('DOMContentLoaded', () => {
            const lazyImages = document.querySelectorAll('img.lazy');
            lazyImages.forEach(img => imageObserver.observe(img));
        });
    }
    
    // Service Worker para cache offline (se suportado)
    if ('serviceWorker' in navigator && window.location.protocol === 'https:') {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => console.log('SW registered:', registration))
                .catch(error => console.log('SW registration failed:', error));
        });
    }
    
    // Otimizações de Performance
    document.addEventListener('DOMContentLoaded', () => {
        // Preconnect para recursos externos
        const preconnectLinks = [
            'https://fonts.googleapis.com',
            'https://fonts.gstatic.com',
            'https://cdn.jsdelivr.net'
        ];
        
        preconnectLinks.forEach(href => {
            const link = document.createElement('link');
            link.rel = 'preconnect';
            link.href = href;
            document.head.appendChild(link);
        });
        
        // Prefetch para páginas comuns
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                const prefetchPages = ['/produtos/', '/pedidos/', '/dashboard/'];
                prefetchPages.forEach(page => {
                    const link = document.createElement('link');
                    link.rel = 'prefetch';
                    link.href = page;
                    document.head.appendChild(link);
                });
            });
        }
    });
    
})();