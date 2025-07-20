/**
 * Sistema de Lazy Loading para imagens
 */

document.addEventListener('DOMContentLoaded', function() {
    // Configurar Intersection Observer para lazy loading
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                
                // Mostrar placeholder de loading
                img.classList.add('loading');
                
                // Carregar imagem
                if (img.dataset.src) {
                    const newImg = new Image();
                    newImg.onload = function() {
                        img.src = this.src;
                        img.classList.remove('loading');
                        img.classList.add('loaded');
                    };
                    newImg.onerror = function() {
                        img.src = '/static/images/placeholder-pizza.svg';
                        img.classList.remove('loading');
                        img.classList.add('error');
                    };
                    newImg.src = img.dataset.src;
                    
                    // Parar de observar esta imagem
                    observer.unobserve(img);
                }
            }
        });
    }, {
        root: null,
        rootMargin: '50px',
        threshold: 0.01
    });

    // Observar todas as imagens com lazy loading
    const lazyImages = document.querySelectorAll('img[data-src]');
    lazyImages.forEach(img => {
        imageObserver.observe(img);
    });
});

// Adicionar estilos para lazy loading
const style = document.createElement('style');
style.textContent = `
    img[data-src] {
        background: #f3f4f6;
        min-height: 200px;
    }
    
    img.loading {
        position: relative;
        overflow: hidden;
    }
    
    img.loading::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent
        );
        animation: shimmer 1.5s infinite;
    }
    
    @keyframes shimmer {
        0% {
            transform: translateX(0);
        }
        100% {
            transform: translateX(200%);
        }
    }
    
    img.loaded {
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);