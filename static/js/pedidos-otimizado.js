// Pedidos Otimizado - Alpine.js Component
function pedidoForm() {
    return {
        // Estado inicial
        tipoPedido: 'delivery',
        categoriaAtiva: 'pizzas',
        buscaProduto: '',
        formaPagamento: '',
        trocoPara: 0,
        observacoes: '',
        mostrarModalConfirmacao: false,
        
        // Carrinho
        carrinho: [],
        subtotal: 0,
        taxaEntrega: 5,
        desconto: 0,
        total: 0,
        
        // Dados do formulário
        cliente: {
            nome: '',
            telefone: '',
            email: '',
            cpf: ''
        },
        
        endereco: {
            cep: '',
            rua: '',
            numero: '',
            complemento: '',
            bairro: '',
            cidade: '',
            estado: '',
            referencia: ''
        },
        
        // Produtos (carregados via API)
        produtosPorCategoria: {
            pizzas: [],
            bebidas: [],
            bordas: []
        },
        
        // Cache de produtos
        produtosCache: new Map(),
        
        // Inicialização
        init() {
            // Carregar produtos de forma assíncrona
            this.carregarProdutos();
            
            // Restaurar carrinho do localStorage
            this.restaurarCarrinho();
            
            // Configurar listeners otimizados
            this.configurarListeners();
            
            // Watch para recalcular total
            this.$watch('carrinho', () => this.calcularTotal());
            this.$watch('tipoPedido', (value) => {
                if (value !== 'delivery') {
                    this.taxaEntrega = 0;
                } else {
                    this.taxaEntrega = 5;
                }
            });
        },
        
        // Carregar produtos via API com cache
        async carregarProdutos() {
            try {
                // Verificar cache primeiro
                const cacheKey = 'produtos_pedido';
                const cached = localStorage.getItem(cacheKey);
                const cacheTime = localStorage.getItem(cacheKey + '_time');
                
                // Cache válido por 10 minutos
                if (cached && cacheTime && (Date.now() - parseInt(cacheTime)) < 600000) {
                    this.produtosPorCategoria = JSON.parse(cached);
                    return;
                }
                
                // Buscar da API
                const response = await fetch('/api/produtos/produtos/para_pedido/');
                const data = await response.json();
                
                this.produtosPorCategoria = data;
                
                // Salvar no cache
                localStorage.setItem(cacheKey, JSON.stringify(data));
                localStorage.setItem(cacheKey + '_time', Date.now().toString());
                
            } catch (error) {
                console.error('Erro ao carregar produtos:', error);
                Alpine.store('app').showToast('Erro ao carregar produtos', 'error');
            }
        },
        
        // Produtos filtrados com memoização
        get produtosFiltrados() {
            const produtos = this.produtosPorCategoria[this.categoriaAtiva] || [];
            
            if (!this.buscaProduto) {
                return produtos;
            }
            
            const busca = this.buscaProduto.toLowerCase();
            return produtos.filter(p => 
                p.nome.toLowerCase().includes(busca) ||
                (p.ingredientes && p.ingredientes.toLowerCase().includes(busca))
            );
        },
        
        // Adicionar produto simples (otimizado)
        adicionarProdutoSimples(id, nome, preco) {
            const itemExistente = this.carrinho.find(item => 
                item.id === id && item.tipo === 'simples'
            );
            
            if (itemExistente) {
                itemExistente.quantidade++;
                itemExistente.subtotal = itemExistente.quantidade * itemExistente.preco;
            } else {
                this.carrinho.push({
                    id: id,
                    nome: nome,
                    preco: preco,
                    quantidade: 1,
                    subtotal: preco,
                    tipo: 'simples'
                });
            }
            
            this.salvarCarrinho();
            Alpine.store('app').showToast(`${nome} adicionado ao carrinho`, 'success');
        },
        
        // Adicionar pizza (com tamanho)
        adicionarPizza(id, nome, tamanho, preco, ingredientes) {
            const itemId = `pizza_${id}_${tamanho}`;
            const itemExistente = this.carrinho.find(item => item.id === itemId);
            
            if (itemExistente) {
                itemExistente.quantidade++;
                itemExistente.subtotal = itemExistente.quantidade * itemExistente.preco;
            } else {
                this.carrinho.push({
                    id: itemId,
                    produtoId: id,
                    nome: `${nome} (${tamanho})`,
                    preco: preco,
                    quantidade: 1,
                    subtotal: preco,
                    tipo: 'pizza',
                    tamanho: tamanho,
                    ingredientes: ingredientes
                });
            }
            
            this.salvarCarrinho();
            Alpine.store('app').showToast(`Pizza ${nome} adicionada`, 'success');
        },
        
        // Remover item (otimizado)
        removerItem(itemId) {
            const index = this.carrinho.findIndex(item => item.id === itemId);
            if (index > -1) {
                const item = this.carrinho[index];
                this.carrinho.splice(index, 1);
                this.salvarCarrinho();
                Alpine.store('app').showToast(`${item.nome} removido`, 'info');
            }
        },
        
        // Alterar quantidade (otimizado)
        alterarQuantidade(itemId, delta) {
            const item = this.carrinho.find(i => i.id === itemId);
            if (!item) return;
            
            item.quantidade = Math.max(1, item.quantidade + delta);
            item.subtotal = item.quantidade * item.preco;
            
            this.salvarCarrinho();
        },
        
        // Calcular total (otimizado)
        calcularTotal() {
            this.subtotal = this.carrinho.reduce((sum, item) => sum + item.subtotal, 0);
            this.total = this.subtotal + this.taxaEntrega - this.desconto;
            
            // Atualizar UI
            this.atualizarUI();
        },
        
        // Atualizar UI de forma otimizada
        atualizarUI() {
            // Usar requestAnimationFrame para otimizar renderização
            requestAnimationFrame(() => {
                // Atualizar valores
                document.getElementById('carrinho-subtotal').textContent = 
                    PizzariaUtils.formatCurrency(this.subtotal);
                document.getElementById('carrinho-total').textContent = 
                    PizzariaUtils.formatCurrency(this.total);
                
                // Mostrar/ocultar taxa de entrega
                const taxaContainer = document.getElementById('taxa-entrega-container');
                if (this.tipoPedido === 'delivery' && this.taxaEntrega > 0) {
                    taxaContainer.style.display = 'flex';
                    document.getElementById('taxa-entrega-valor').textContent = 
                        PizzariaUtils.formatCurrency(this.taxaEntrega);
                } else {
                    taxaContainer.style.display = 'none';
                }
                
                // Habilitar/desabilitar botão finalizar
                const btnFinalizar = document.getElementById('btn-finalizar-pedido');
                btnFinalizar.disabled = this.carrinho.length === 0;
            });
        },
        
        // Salvar carrinho no localStorage
        salvarCarrinho() {
            localStorage.setItem('carrinho_pedido', JSON.stringify(this.carrinho));
            this.calcularTotal();
        },
        
        // Restaurar carrinho do localStorage
        restaurarCarrinho() {
            const saved = localStorage.getItem('carrinho_pedido');
            if (saved) {
                try {
                    this.carrinho = JSON.parse(saved);
                    this.calcularTotal();
                } catch (e) {
                    console.error('Erro ao restaurar carrinho:', e);
                }
            }
        },
        
        // Limpar carrinho
        limparCarrinho() {
            if (confirm('Deseja realmente limpar o carrinho?')) {
                this.carrinho = [];
                localStorage.removeItem('carrinho_pedido');
                Alpine.store('app').showToast('Carrinho limpo', 'info');
            }
        },
        
        // Validar formulário
        validarFormulario() {
            let valido = true;
            const erros = [];
            
            // Validar cliente
            if (!this.cliente.nome) {
                erros.push('Nome do cliente é obrigatório');
                valido = false;
            }
            
            if (!this.cliente.telefone) {
                erros.push('Telefone é obrigatório');
                valido = false;
            }
            
            // Validar endereço se for delivery
            if (this.tipoPedido === 'delivery') {
                if (!this.endereco.rua || !this.endereco.numero || !this.endereco.bairro) {
                    erros.push('Endereço completo é obrigatório para delivery');
                    valido = false;
                }
            }
            
            // Validar forma de pagamento
            if (!this.formaPagamento) {
                erros.push('Selecione uma forma de pagamento');
                valido = false;
            }
            
            // Mostrar erros
            if (!valido) {
                erros.forEach(erro => Alpine.store('app').showToast(erro, 'error'));
            }
            
            return valido;
        },
        
        // Finalizar pedido
        async finalizarPedido() {
            if (!this.validarFormulario()) {
                this.mostrarModalConfirmacao = false;
                return;
            }
            
            try {
                // Montar dados do pedido
                const pedidoData = {
                    tipo: this.tipoPedido,
                    cliente: this.cliente,
                    endereco: this.tipoPedido === 'delivery' ? this.endereco : null,
                    itens: this.carrinho.map(item => ({
                        produto_id: item.produtoId || item.id,
                        quantidade: item.quantidade,
                        preco_unitario: item.preco,
                        observacao: item.observacao || ''
                    })),
                    forma_pagamento: this.formaPagamento,
                    troco_para: this.formaPagamento === 'dinheiro' ? this.trocoPara : null,
                    observacoes: this.observacoes,
                    subtotal: this.subtotal,
                    taxa_entrega: this.taxaEntrega,
                    desconto: this.desconto,
                    total: this.total
                };
                
                // Enviar pedido
                const response = await fetch('/api/pedidos/criar_pedido_seguro/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': PizzariaUtils.getCookie('csrftoken')
                    },
                    body: JSON.stringify(pedidoData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    // Limpar carrinho
                    this.carrinho = [];
                    localStorage.removeItem('carrinho_pedido');
                    
                    // Mostrar sucesso
                    Alpine.store('app').showToast('Pedido criado com sucesso!', 'success');
                    
                    // Redirecionar
                    setTimeout(() => {
                        window.location.href = `/pedidos/${result.pedido_id}/`;
                    }, 1500);
                } else {
                    Alpine.store('app').showToast(result.error || 'Erro ao criar pedido', 'error');
                }
                
            } catch (error) {
                console.error('Erro ao finalizar pedido:', error);
                Alpine.store('app').showToast('Erro ao processar pedido', 'error');
            } finally {
                this.mostrarModalConfirmacao = false;
            }
        },
        
        // Configurar listeners otimizados
        configurarListeners() {
            // Debounce para busca
            let searchTimeout;
            this.$watch('buscaProduto', (value) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    // A busca é feita automaticamente pelo getter produtosFiltrados
                }, 300);
            });
            
            // Listener para botão limpar carrinho
            document.getElementById('btn-limpar-carrinho')?.addEventListener('click', 
                () => this.limparCarrinho()
            );
            
            // Listener para botão finalizar
            document.getElementById('btn-finalizar-pedido')?.addEventListener('click', 
                () => this.mostrarModalConfirmacao = true
            );
        }
    };
}

// Funções globais para compatibilidade
window.adicionarProdutoSimples = function(id, nome, preco) {
    const component = Alpine.$data(document.querySelector('[x-data]'));
    component.adicionarProdutoSimples(id, nome, preco);
};

window.removerItem = function(itemId) {
    const component = Alpine.$data(document.querySelector('[x-data]'));
    component.removerItem(itemId);
};

window.alterarQuantidade = function(itemId, delta) {
    const component = Alpine.$data(document.querySelector('[x-data]'));
    component.alterarQuantidade(itemId, delta);
};

// Buscar CEP com cache
window.buscarCEP = async function() {
    const cepInput = document.getElementById('endereco_cep');
    const cep = cepInput.value.replace(/\D/g, '');
    
    if (cep.length !== 8) {
        Alpine.store('app').showToast('CEP inválido', 'error');
        return;
    }
    
    try {
        // Verificar cache primeiro
        const cached = localStorage.getItem(`cep_${cep}`);
        if (cached) {
            const data = JSON.parse(cached);
            preencherEndereco(data);
            return;
        }
        
        // Buscar da API
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();
        
        if (data.erro) {
            Alpine.store('app').showToast('CEP não encontrado', 'error');
        } else {
            preencherEndereco(data);
            // Salvar no cache
            localStorage.setItem(`cep_${cep}`, JSON.stringify(data));
        }
    } catch (error) {
        console.error('Erro ao buscar CEP:', error);
        Alpine.store('app').showToast('Erro ao buscar CEP', 'error');
    }
};

function preencherEndereco(data) {
    document.getElementById('endereco_rua').value = data.logradouro || '';
    document.getElementById('endereco_bairro').value = data.bairro || '';
    document.getElementById('endereco_cidade').value = data.localidade || '';
    document.getElementById('endereco_estado').value = data.uf || '';
}