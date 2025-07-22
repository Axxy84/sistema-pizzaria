// PWA Install Helper
class PWAInstaller {
    constructor() {
        this.deferredPrompt = null;
        this.isInstalled = false;
        this.init();
    }

    init() {
        // Verifica se já está instalado
        if (window.matchMedia('(display-mode: standalone)').matches) {
            this.isInstalled = true;
            return;
        }

        // Detecta se está no iOS
        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
        if (isIOS && !window.navigator.standalone) {
            this.showIOSInstallInstructions();
        }

        // Captura evento de instalação
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallButton();
        });

        // Detecta quando foi instalado
        window.addEventListener('appinstalled', () => {
            this.isInstalled = true;
            this.hideInstallButton();
            this.showSuccessMessage();
        });
    }

    showInstallButton() {
        // Cria botão flutuante de instalação
        const button = document.createElement('div');
        button.id = 'pwa-install-button';
        button.innerHTML = `
            <button class="fixed bottom-4 right-4 bg-pizza-600 text-white px-6 py-3 rounded-full shadow-lg hover:bg-pizza-700 transition-all duration-300 flex items-center space-x-2 z-50">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8l-8 8-8-8" />
                </svg>
                <span>Instalar App</span>
            </button>
        `;
        
        document.body.appendChild(button);
        
        button.addEventListener('click', () => this.install());
        
        // Mostra dica após 30 segundos
        setTimeout(() => {
            if (!this.isInstalled && this.deferredPrompt) {
                this.showInstallTooltip();
            }
        }, 30000);
    }

    hideInstallButton() {
        const button = document.getElementById('pwa-install-button');
        if (button) {
            button.remove();
        }
    }

    async install() {
        if (!this.deferredPrompt) return;
        
        this.deferredPrompt.prompt();
        const { outcome } = await this.deferredPrompt.userChoice;
        
        if (outcome === 'accepted') {
            console.log('PWA instalado com sucesso');
        } else {
            console.log('Instalação cancelada pelo usuário');
        }
        
        this.deferredPrompt = null;
        this.hideInstallButton();
    }

    showIOSInstallInstructions() {
        // Mostra instruções específicas para iOS
        const instructions = document.createElement('div');
        instructions.id = 'ios-install-instructions';
        instructions.className = 'fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 shadow-lg z-50';
        instructions.innerHTML = `
            <div class="max-w-sm mx-auto text-center">
                <p class="text-sm text-gray-600 mb-2">Para instalar este app no seu iPhone/iPad:</p>
                <div class="flex items-center justify-center space-x-2 text-pizza-600">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 2a1 1 0 011 1v5.586l2.293-2.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 8.586V3a1 1 0 011-1z"/>
                        <path d="M5 12a1 1 0 011 1v3h8v-3a1 1 0 112 0v3a2 2 0 01-2 2H6a2 2 0 01-2-2v-3a1 1 0 011-1z"/>
                    </svg>
                    <span class="text-sm font-medium">Toque em Compartilhar → Adicionar à Tela Inicial</span>
                </div>
                <button onclick="document.getElementById('ios-install-instructions').remove()" class="mt-2 text-xs text-gray-500 underline">Fechar</button>
            </div>
        `;
        
        // Mostra apenas na primeira visita
        if (!localStorage.getItem('ios-install-shown')) {
            setTimeout(() => {
                document.body.appendChild(instructions);
                localStorage.setItem('ios-install-shown', 'true');
                
                // Remove após 10 segundos
                setTimeout(() => {
                    instructions.remove();
                }, 10000);
            }, 5000);
        }
    }

    showInstallTooltip() {
        const tooltip = document.createElement('div');
        tooltip.className = 'fixed bottom-20 right-4 bg-gray-900 text-white text-sm px-4 py-2 rounded-lg shadow-lg z-50';
        tooltip.innerHTML = '💡 Instale o app para acesso rápido!';
        document.body.appendChild(tooltip);
        
        setTimeout(() => tooltip.remove(), 5000);
    }

    showSuccessMessage() {
        // Usa o sistema de toast do Alpine.js se disponível
        if (window.Alpine && Alpine.store('app')) {
            Alpine.store('app').showToast('App instalado com sucesso! 🎉', 'success');
        } else {
            alert('App instalado com sucesso!');
        }
    }
}

// Inicializa quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.pwaInstaller = new PWAInstaller();
});