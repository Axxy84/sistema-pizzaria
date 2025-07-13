// JavaScript Simplificado para Pedidos
function pedidoForm() {
    return {
        // Estado do pedido
        tipoPedido: 'delivery',
        formaPagamento: 'dinheiro',
        trocoPara: '',
        observacoes: '',
        
        // Dados do cliente
        cliente: {
            nome: '',
            telefone: '',
            endereco_simples: '',
            referencia: ''
        },
        
        // Produtos
        produtosPorCategoria: {
            pizzas: [],
            bebidas: [],
            bordas: []
        },
        categoriaAtiva: 'pizzas',
        produtosFiltrados: [],
        
        // Carrinho
        carrinho: [],
        subtotal: 0,
        taxaEntrega: 5,
        total: 0,
        
        // Modal
        mostrarModalConfirmacao: false,
        
        // Inicialização
        async init() {
            console.log('Inicializando pedidoForm...');
            console.log('Categoria ativa inicial:', this.categoriaAtiva);
            await this.carregarProdutos();
            this.atualizarProdutosFiltrados();
            this.calcularTotal();
            console.log('Inicialização completa');
        },
        
        // Carregar produtos da API
        async carregarProdutos() {
            try {
                console.log('Iniciando carregamento de produtos...');
                const response = await fetch('/api/produtos/produtos/para_pedido/');
                const data = await response.json();
                
                console.log('Dados recebidos da API:', data);
                
                // A API já retorna os produtos organizados por categoria
                if (data) {
                    this.produtosPorCategoria = {
                        pizzas: data.pizzas || [],
                        bebidas: data.bebidas || [],
                        bordas: data.bordas || []
                    };
                    
                    console.log('Produtos organizados:', this.produtosPorCategoria);
                    console.log('Total de pizzas:', this.produtosPorCategoria.pizzas.length);
                    console.log('Total de bebidas:', this.produtosPorCategoria.bebidas.length);
                    console.log('Total de bordas:', this.produtosPorCategoria.bordas.length);
                    
                    // Forçar atualização após carregar os dados
                    this.$nextTick(() => {
                        this.atualizarProdutosFiltrados();
                    });
                }
            } catch (error) {
                console.error('Erro ao carregar produtos:', error);
                // Usar produtos de teste se falhar
                this.usarProdutosTeste();
            }
        },
        
        // Produtos de teste como fallback
        usarProdutosTeste() {
            this.produtosPorCategoria = {
                pizzas: [
                    {
                        id: 1,
                        nome: 'Margherita',
                        descricao: 'Molho, mussarela, tomate, manjericão',
                        categoria: 'Pizza',
                        tamanhos: [
                            {id: 1, nome: 'P', preco: 25},
                            {id: 2, nome: 'M', preco: 35},
                            {id: 3, nome: 'G', preco: 45}
                        ]
                    },
                    {
                        id: 2,
                        nome: 'Calabresa',
                        descricao: 'Molho, mussarela, calabresa, cebola',
                        categoria: 'Pizza',
                        tamanhos: [
                            {id: 4, nome: 'P', preco: 28},
                            {id: 5, nome: 'M', preco: 38},
                            {id: 6, nome: 'G', preco: 48}
                        ]
                    }
                ],
                bebidas: [
                    {id: 3, nome: 'Coca-Cola 2L', categoria: 'Bebida', preco: 12},
                    {id: 4, nome: 'Água Mineral', categoria: 'Bebida', preco: 3}
                ],
                bordas: [
                    {id: 5, nome: 'Borda Catupiry', categoria: 'Borda', preco: 8}
                ]
            };
        },
        
        // Atualizar produtos filtrados por categoria
        atualizarProdutosFiltrados() {
            console.log('Atualizando produtos filtrados para categoria:', this.categoriaAtiva);
            this.produtosFiltrados = this.produtosPorCategoria[this.categoriaAtiva] || [];
            console.log('Produtos filtrados:', this.produtosFiltrados);
            console.log('Total de produtos na categoria ativa:', this.produtosFiltrados.length);
        },
        
        // Adicionar pizza ao carrinho
        adicionarAoCarrinho(produto, tamanho) {
            const item = {
                id: Date.now(),
                produto_id: produto.id,
                nome: produto.nome,
                tamanho: tamanho.nome,
                preco: tamanho.preco,
                quantidade: 1,
                tipo: 'pizza'
            };
            
            this.carrinho.push(item);
            this.calcularTotal();
            
            // Feedback visual
            this.mostrarFeedback(`${produto.nome} (${tamanho.nome}) adicionada!`);
        },
        
        // Adicionar produto simples ao carrinho
        adicionarProdutoAoCarrinho(produto) {
            const item = {
                id: Date.now(),
                produto_id: produto.id,
                nome: produto.nome,
                preco: produto.preco,
                quantidade: 1,
                tipo: produto.categoria.toLowerCase()
            };
            
            this.carrinho.push(item);
            this.calcularTotal();
            
            // Feedback visual
            this.mostrarFeedback(`${produto.nome} adicionado!`);
        },
        
        // Remover item do carrinho
        removerItem(itemId) {
            this.carrinho = this.carrinho.filter(item => item.id !== itemId);
            this.calcularTotal();
        },
        
        // Alterar quantidade
        alterarQuantidade(itemId, delta) {
            const item = this.carrinho.find(i => i.id === itemId);
            if (item) {
                item.quantidade += delta;
                if (item.quantidade <= 0) {
                    this.removerItem(itemId);
                } else {
                    this.calcularTotal();
                }
            }
        },
        
        // Calcular totais
        calcularTotal() {
            this.subtotal = this.carrinho.reduce((sum, item) => {
                return sum + (item.preco * item.quantidade);
            }, 0);
            
            const entrega = this.tipoPedido === 'delivery' ? this.taxaEntrega : 0;
            this.total = this.subtotal + entrega;
        },
        
        // Validar pedido
        validarPedido() {
            const erros = [];
            
            if (!this.cliente.nome) erros.push('Nome é obrigatório');
            if (!this.cliente.telefone) erros.push('Telefone é obrigatório');
            if (this.tipoPedido === 'delivery' && !this.cliente.endereco_simples) {
                erros.push('Endereço é obrigatório para delivery');
            }
            if (this.carrinho.length === 0) erros.push('Carrinho está vazio');
            if (!this.formaPagamento) erros.push('Selecione uma forma de pagamento');
            
            return erros;
        },
        
        // Finalizar pedido
        async finalizarPedido() {
            // Validar
            const erros = this.validarPedido();
            if (erros.length > 0) {
                alert('Por favor, corrija:\n' + erros.join('\n'));
                return;
            }
            
            // Preparar dados
            const dados = {
                tipo: this.tipoPedido,
                cliente: this.cliente,
                itens: this.carrinho,
                forma_pagamento: this.formaPagamento,
                troco_para: this.formaPagamento === 'dinheiro' ? this.trocoPara : null,
                observacoes: this.observacoes,
                subtotal: this.subtotal,
                taxa_entrega: this.tipoPedido === 'delivery' ? this.taxaEntrega : 0,
                total: this.total
            };
            
            try {
                const response = await fetch('/api/pedidos/criar/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCookie('csrftoken')
                    },
                    body: JSON.stringify(dados)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    alert('Pedido criado com sucesso!');
                    window.location.href = `/pedidos/${result.id}/`;
                } else {
                    alert('Erro ao criar pedido. Tente novamente.');
                }
            } catch (error) {
                console.error('Erro:', error);
                alert('Erro ao processar pedido.');
            }
            
            this.mostrarModalConfirmacao = false;
        },
        
        // Utilitários
        getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
        
        mostrarFeedback(mensagem) {
            // Implementar toast notification
            console.log(mensagem);
        },
        
        // Modal meio a meio (simplificado)
        abrirModalMeioAMeio(pizza) {
            alert('Função meio a meio em desenvolvimento');
        }
    };
}