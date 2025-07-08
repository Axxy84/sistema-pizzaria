// Base JavaScript for Pizzaria Management System
// Alpine.js components and utilities

document.addEventListener('alpine:init', () => {
    
    // Global App State
    Alpine.store('app', {
        loading: false,
        
        // Methods
        setLoading(state) {
            this.loading = state;
        },
        
        // Show toast notification
        showToast(message, type = 'info', duration = 5000) {
            window.dispatchEvent(new CustomEvent('show-toast', {
                detail: { message, type, duration }
            }));
        },
        
        // Show alert in messages area
        showAlert(message, type = 'info') {
            // Update the main Alpine component
            const appComponent = document.querySelector('[x-data]')?.__x?.$data;
            if (appComponent) {
                appComponent.alertMessage = message;
                appComponent.alertType = type;
                appComponent.showAlert = true;
            }
        }
    });

    // Modal Component
    Alpine.data('modal', (initialOpen = false) => ({
        open: initialOpen,
        
        show() {
            this.open = true;
            document.body.style.overflow = 'hidden';
        },
        
        hide() {
            this.open = false;
            document.body.style.overflow = 'auto';
        },
        
        toggle() {
            this.open ? this.hide() : this.show();
        }
    }));

    // Dropdown Component
    Alpine.data('dropdown', () => ({
        open: false,
        
        toggle() {
            this.open = !this.open;
        },
        
        close() {
            this.open = false;
        }
    }));

    // Search Component
    Alpine.data('search', (options = {}) => ({
        query: '',
        results: [],
        loading: false,
        debounceTimer: null,
        
        async search() {
            if (this.query.length < (options.minLength || 2)) {
                this.results = [];
                return;
            }
            
            this.loading = true;
            
            // Clear previous debounce
            clearTimeout(this.debounceTimer);
            
            // Debounce search
            this.debounceTimer = setTimeout(async () => {
                try {
                    const response = await fetch(`${options.url}?q=${encodeURIComponent(this.query)}`);
                    this.results = await response.json();
                } catch (error) {
                    console.error('Search error:', error);
                    Alpine.store('app').showToast('Erro na busca', 'error');
                } finally {
                    this.loading = false;
                }
            }, options.debounce || 300);
        },
        
        clear() {
            this.query = '';
            this.results = [];
        }
    }));

    // Form Component
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
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    Alpine.store('app').showToast(data.message || 'Salvo com sucesso!', 'success');
                    if (options.onSuccess) {
                        options.onSuccess(data);
                    }
                } else {
                    this.errors = data.errors || {};
                    Alpine.store('app').showToast(data.message || 'Erro ao salvar', 'error');
                }
            } catch (error) {
                console.error('Form submission error:', error);
                Alpine.store('app').showToast('Erro de conexão', 'error');
            } finally {
                this.loading = false;
            }
        },
        
        clearErrors() {
            this.errors = {};
        }
    }));

    // Table Component
    Alpine.data('table', (options = {}) => ({
        data: [],
        loading: false,
        page: 1,
        perPage: options.perPage || 10,
        total: 0,
        sortBy: options.defaultSort || 'id',
        sortOrder: 'asc',
        filters: {},
        
        async loadData() {
            this.loading = true;
            
            try {
                const params = new URLSearchParams({
                    page: this.page,
                    per_page: this.perPage,
                    sort_by: this.sortBy,
                    sort_order: this.sortOrder,
                    ...this.filters
                });
                
                const response = await fetch(`${options.url}?${params}`);
                const result = await response.json();
                
                this.data = result.data || result.results || [];
                this.total = result.total || result.count || 0;
            } catch (error) {
                console.error('Table load error:', error);
                Alpine.store('app').showToast('Erro ao carregar dados', 'error');
            } finally {
                this.loading = false;
            }
        },
        
        sort(column) {
            if (this.sortBy === column) {
                this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortBy = column;
                this.sortOrder = 'asc';
            }
            this.page = 1;
            this.loadData();
        },
        
        filter(filters) {
            this.filters = { ...this.filters, ...filters };
            this.page = 1;
            this.loadData();
        },
        
        changePage(newPage) {
            this.page = newPage;
            this.loadData();
        },
        
        get totalPages() {
            return Math.ceil(this.total / this.perPage);
        },
        
        init() {
            this.loadData();
        }
    }));

    // Tabs Component
    Alpine.data('tabs', (defaultTab = 0) => ({
        activeTab: defaultTab,
        
        setActive(index) {
            this.activeTab = index;
        },
        
        isActive(index) {
            return this.activeTab === index;
        }
    }));

    // File Upload Component
    Alpine.data('fileUpload', (options = {}) => ({
        files: [],
        uploading: false,
        progress: 0,
        
        async upload(files) {
            this.uploading = true;
            this.progress = 0;
            
            const formData = new FormData();
            Array.from(files).forEach(file => {
                formData.append('files[]', file);
            });
            
            try {
                const xhr = new XMLHttpRequest();
                
                xhr.upload.onprogress = (e) => {
                    if (e.lengthComputable) {
                        this.progress = Math.round((e.loaded / e.total) * 100);
                    }
                };
                
                xhr.onload = () => {
                    if (xhr.status === 200) {
                        const response = JSON.parse(xhr.responseText);
                        this.files = response.files || [];
                        Alpine.store('app').showToast('Upload concluído!', 'success');
                        if (options.onSuccess) {
                            options.onSuccess(response);
                        }
                    } else {
                        Alpine.store('app').showToast('Erro no upload', 'error');
                    }
                    this.uploading = false;
                    this.progress = 0;
                };
                
                xhr.onerror = () => {
                    Alpine.store('app').showToast('Erro de conexão', 'error');
                    this.uploading = false;
                    this.progress = 0;
                };
                
                xhr.open('POST', options.url);
                xhr.setRequestHeader('X-CSRFToken', getCsrfToken());
                xhr.send(formData);
                
            } catch (error) {
                console.error('Upload error:', error);
                Alpine.store('app').showToast('Erro no upload', 'error');
                this.uploading = false;
                this.progress = 0;
            }
        }
    }));
});

// Utility Functions
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(date));
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Global event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide Django messages after 5 seconds
    const messages = document.querySelectorAll('.messages .message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
    
    // Handle AJAX errors globally
    window.addEventListener('unhandledrejection', function(event) {
        console.error('Unhandled promise rejection:', event.reason);
        Alpine.store('app').showToast('Erro inesperado', 'error');
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Escape key to close modals/dropdowns
    if (e.key === 'Escape') {
        // Close all open modals and dropdowns
        const event = new CustomEvent('close-all');
        document.dispatchEvent(event);
    }
    
    // Ctrl+S to save (prevent default)
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        // Trigger save if there's a form
        const saveButton = document.querySelector('[data-save]');
        if (saveButton) {
            saveButton.click();
        }
    }
});

// Export utilities for global use
window.PizzariaUtils = {
    formatCurrency,
    formatDate,
    debounce,
    getCsrfToken
};