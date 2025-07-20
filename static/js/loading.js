/**
 * Sistema de Loading Global da Pizzaria
 */

class LoadingManager {
    constructor() {
        this.createLoadingOverlay();
        this.setupInterceptors();
        this.setupPageTransitions();
    }

    createLoadingOverlay() {
        // Criar overlay de loading se não existir
        if (!document.getElementById('global-loading')) {
            const overlay = document.createElement('div');
            overlay.id = 'global-loading';
            overlay.className = 'loading-overlay';
            overlay.innerHTML = `
                <div class="pizza-loader">
                    <div class="pizza-slice"></div>
                    <div class="loading-text">Carregando<span class="loading-dots"></span></div>
                </div>
            `;
            document.body.appendChild(overlay);
        }

        // Criar barra de progresso se não existir
        if (!document.getElementById('page-loading-bar')) {
            const progressBar = document.createElement('div');
            progressBar.id = 'page-loading-bar';
            progressBar.className = 'page-loading-bar';
            document.body.appendChild(progressBar);
        }
    }

    show(message = 'Carregando') {
        const overlay = document.getElementById('global-loading');
        const loadingText = overlay.querySelector('.loading-text');
        if (loadingText) {
            loadingText.innerHTML = `${message}<span class="loading-dots"></span>`;
        }
        overlay.classList.add('active');
    }

    hide() {
        const overlay = document.getElementById('global-loading');
        overlay.classList.remove('active');
    }

    showProgress() {
        const bar = document.getElementById('page-loading-bar');
        bar.classList.add('loading');
        bar.style.width = '0%';
        
        // Resetar após a animação
        setTimeout(() => {
            bar.classList.remove('loading');
            bar.style.width = '0%';
        }, 2000);
    }

    setupInterceptors() {
        // Interceptar fetch
        const originalFetch = window.fetch;
        let activeRequests = 0;

        window.fetch = async (...args) => {
            // Verificar se deve mostrar loading
            const showLoading = !args[1]?.skipLoading;
            
            if (showLoading) {
                activeRequests++;
                if (activeRequests === 1) {
                    this.show('Carregando dados');
                }
            }

            try {
                const response = await originalFetch(...args);
                return response;
            } finally {
                if (showLoading) {
                    activeRequests--;
                    if (activeRequests === 0) {
                        setTimeout(() => this.hide(), 300);
                    }
                }
            }
        };

        // Interceptar XMLHttpRequest
        const originalXHR = window.XMLHttpRequest;
        const self = this;

        window.XMLHttpRequest = function() {
            const xhr = new originalXHR();
            const originalOpen = xhr.open;
            const originalSend = xhr.send;
            let showLoading = true;

            xhr.open = function(...args) {
                // Verificar se é uma requisição que deve mostrar loading
                if (args[1] && args[1].includes('skipLoading=true')) {
                    showLoading = false;
                }
                return originalOpen.apply(this, args);
            };

            xhr.send = function(...args) {
                if (showLoading) {
                    activeRequests++;
                    if (activeRequests === 1) {
                        self.show('Carregando dados');
                    }
                }

                xhr.addEventListener('loadend', () => {
                    if (showLoading) {
                        activeRequests--;
                        if (activeRequests === 0) {
                            setTimeout(() => self.hide(), 300);
                        }
                    }
                });

                return originalSend.apply(this, args);
            };

            return xhr;
        };
    }

    setupPageTransitions() {
        // Mostrar loading em navegação de página
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link && link.href && !link.target && !link.hasAttribute('data-no-loading')) {
                // Verificar se é um link interno
                const currentHost = window.location.host;
                const linkHost = new URL(link.href).host;
                
                if (currentHost === linkHost) {
                    this.showProgress();
                }
            }
        });

        // Mostrar loading em submissão de formulários
        document.addEventListener('submit', (e) => {
            const form = e.target;
            if (!form.hasAttribute('data-no-loading')) {
                this.show('Processando');
            }
        });
    }

    // Métodos utilitários
    showInlineLoader(element, message = 'Carregando...') {
        const originalContent = element.innerHTML;
        element.innerHTML = `${message} <span class="inline-loader"></span>`;
        element.disabled = true;
        
        return () => {
            element.innerHTML = originalContent;
            element.disabled = false;
        };
    }

    addButtonLoader(button) {
        button.classList.add('btn-loading');
        button.disabled = true;
        
        return () => {
            button.classList.remove('btn-loading');
            button.disabled = false;
        };
    }

    createSkeletonLoader(count = 3, type = 'list') {
        const skeletons = [];
        
        for (let i = 0; i < count; i++) {
            if (type === 'list') {
                skeletons.push(`
                    <div class="skeleton-loader p-4 mb-4 rounded-lg">
                        <div class="skeleton-title skeleton-loader"></div>
                        <div class="skeleton-text skeleton-loader"></div>
                        <div class="skeleton-text skeleton-loader" style="width: 80%"></div>
                    </div>
                `);
            } else if (type === 'card') {
                skeletons.push(`
                    <div class="skeleton-loader p-4 rounded-lg">
                        <div class="skeleton-image skeleton-loader"></div>
                        <div class="skeleton-title skeleton-loader"></div>
                        <div class="skeleton-text skeleton-loader"></div>
                    </div>
                `);
            }
        }
        
        return skeletons.join('');
    }
}

// Inicializar o gerenciador de loading
const loadingManager = new LoadingManager();

// Exportar para uso global
window.PizzariaLoading = loadingManager;

// Função helper para facilitar o uso
window.showLoading = (message) => loadingManager.show(message);
window.hideLoading = () => loadingManager.hide();

// Exemplo de uso específico para produtos
window.loadProdutos = async function(url, container) {
    // Mostrar skeleton loader enquanto carrega
    container.innerHTML = loadingManager.createSkeletonLoader(6, 'card');
    
    try {
        const response = await fetch(url, { skipLoading: true });
        const data = await response.json();
        
        // Simular delay mínimo para evitar flicker
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Renderizar produtos
        renderProdutos(data, container);
    } catch (error) {
        container.innerHTML = `
            <div class="text-center py-8">
                <p class="text-red-600">Erro ao carregar produtos</p>
                <button onclick="loadProdutos('${url}', document.getElementById('${container.id}'))" 
                        class="mt-4 btn btn-primary">
                    Tentar novamente
                </button>
            </div>
        `;
    }
};