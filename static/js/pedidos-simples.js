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
        
        // Meio a meio
        modalMeioAMeioMostrar: false,
        modalMeioAMeioPizzaBase: null,
        modalMeioAMeioSabor1: null,
        modalMeioAMeioSabor2: null,
        modalMeioAMeioTamanho: null,
        modalMeioAMeioRegra: 'mais_caro',
        modalMeioAMeioPreco: 0,
        modalMeioAMeioEconomia: 0,
        
        // Busca de sabores
        buscaSabor1: '',
        buscaSabor2: '',
        
        // Loading state
        calculandoPreco: false,
        processandoPedido: false,
        
        // Modal Dados Cliente
        modalDadosCliente: false,
        
        // Modal Pedido Completo
        modalPedidoCompleto: false,
        modalPedido: {
            tipoPizza: 'inteira',
            sabor1: null,
            sabor1Id: null,
            sabor2: null,
            sabor2Id: null,
            tamanhoSelecionado: null,
            tamanhoSelecionadoId: null,
            tamanhos: [],
            borda: null,
            bebidas: {},
            observacoes: '',
            precoPizza: 0,
            total: 0
        },
        
        // Inicialização
        async init() {
            console.log('Inicializando pedidoForm...');
            console.log('Categoria ativa inicial:', this.categoriaAtiva);
            console.log('modalMeioAMeio inicializado');
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
            // Toast notification simples
            const toast = document.createElement('div');
            toast.className = 'fixed bottom-4 right-4 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all';
            toast.textContent = mensagem;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        },
        
        // Filtrar sabores (implementação vazia pois já está no template)
        filtrarSabores(numero) {
            // A filtragem é feita diretamente no template com Alpine.js
            console.log(`Filtrando sabores ${numero}`);
        },
        
        // Modal meio a meio
        abrirModalMeioAMeio(pizza) {
            this.modalMeioAMeioMostrar = true;
            this.modalMeioAMeioPizzaBase = pizza;
            this.modalMeioAMeioSabor1 = null;
            this.modalMeioAMeioSabor2 = null;
            this.modalMeioAMeioTamanho = null;
            this.modalMeioAMeioPreco = 0;
            this.modalMeioAMeioEconomia = 0;
            this.buscaSabor1 = '';
            this.buscaSabor2 = '';
            this.calculandoPreco = false;
        },

        fecharModalMeioAMeio() {
            this.modalMeioAMeioMostrar = false;
        },

        selecionarSabor1(pizza) {
            this.modalMeioAMeioSabor1 = pizza;
            // Animar preview da pizza
            this.$nextTick(() => {
                const preview = document.querySelector('.pizza-half-left');
                if (preview) {
                    preview.style.transform = 'scale(1.1)';
                    setTimeout(() => {
                        preview.style.transform = 'scale(1)';
                    }, 200);
                }
            });
            this.calcularPrecoMeioAMeio();
        },

        selecionarSabor2(pizza) {
            this.modalMeioAMeioSabor2 = pizza;
            // Animar preview da pizza
            this.$nextTick(() => {
                const preview = document.querySelector('.pizza-half-right');
                if (preview) {
                    preview.style.transform = 'scale(1.1)';
                    setTimeout(() => {
                        preview.style.transform = 'scale(1)';
                    }, 200);
                }
            });
            this.calcularPrecoMeioAMeio();
        },

        selecionarTamanhoMeioAMeio(tamanho) {
            this.modalMeioAMeioTamanho = tamanho;
            this.calcularPrecoMeioAMeio();
        },

        async calcularPrecoMeioAMeio() {
            if (!this.modalMeioAMeioSabor1 || !this.modalMeioAMeioSabor2 || !this.modalMeioAMeioTamanho) {
                this.modalMeioAMeioPreco = 0;
                this.modalMeioAMeioEconomia = 0;
                return;
            }
            
            // Mostrar loading
            this.calculandoPreco = true;

            try {
                const response = await fetch('/api/pedidos/meio-a-meio/calcular-preco/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: JSON.stringify({
                        sabor_1_id: this.modalMeioAMeioSabor1.id,
                        sabor_2_id: this.modalMeioAMeioSabor2.id,
                        tamanho_id: this.modalMeioAMeioTamanho.id,
                        regra_preco: this.modalMeioAMeioRegra
                    })
                });

                const data = await response.json();
                
                if (data.status === 'success') {
                    this.modalMeioAMeioPreco = data.dados.preco_final;
                    this.modalMeioAMeioEconomia = data.dados.economia;
                } else {
                    console.error('Erro ao calcular preço:', data.message);
                    this.mostrarFeedback(data.message || 'Erro ao calcular preço');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
                this.mostrarFeedback('Erro de conexão');
            } finally {
                // Esconder loading
                this.calculandoPreco = false;
            }
        },

        async adicionarMeioAMeioAoCarrinho() {
            // Validações
            const erros = [];
            
            if (!this.modalMeioAMeioSabor1) {
                erros.push('Selecione o primeiro sabor');
            }
            if (!this.modalMeioAMeioSabor2) {
                erros.push('Selecione o segundo sabor');
            }
            if (!this.modalMeioAMeioTamanho) {
                erros.push('Selecione o tamanho da pizza');
            }
            if (this.modalMeioAMeioSabor1?.id === this.modalMeioAMeioSabor2?.id) {
                erros.push('Selecione sabores diferentes');
            }
            
            if (erros.length > 0) {
                this.mostrarFeedback(erros[0]);
                // Focar no primeiro elemento com erro
                if (!this.modalMeioAMeioSabor1) {
                    document.querySelector('.sabor-section-1 input')?.focus();
                } else if (!this.modalMeioAMeioSabor2) {
                    document.querySelector('.sabor-section-2 input')?.focus();
                } else if (!this.modalMeioAMeioTamanho) {
                    document.querySelector('.tamanho-item')?.focus();
                }
                return;
            }

            // Criar item meio a meio no carrinho
            const itemMeioAMeio = {
                id: `meio_a_meio_${Date.now()}`,
                tipo: 'meio_a_meio',
                nome: `Meio a Meio: ${this.modalMeioAMeioSabor1.nome} + ${this.modalMeioAMeioSabor2.nome}`,
                tamanho: this.modalMeioAMeioTamanho.nome,
                preco: this.modalMeioAMeioPreco,
                quantidade: 1,
                meio_a_meio_data: {
                    is_meio_a_meio: true,
                    sabor_1: {
                        id: this.modalMeioAMeioSabor1.id,
                        nome: this.modalMeioAMeioSabor1.nome
                    },
                    sabor_2: {
                        id: this.modalMeioAMeioSabor2.id,
                        nome: this.modalMeioAMeioSabor2.nome
                    },
                    tamanho: this.modalMeioAMeioTamanho.nome,
                    tamanho_id: this.modalMeioAMeioTamanho.id,
                    regra_preco: this.modalMeioAMeioRegra
                }
            };

            this.carrinho.push(itemMeioAMeio);
            this.calcularTotal();
            this.fecharModalMeioAMeio();
            this.mostrarFeedback('Pizza meio a meio adicionada ao carrinho!');
        },
        
        // === FUNÇÕES DO MODAL PEDIDO COMPLETO ===
        
        // Abrir modal de pedido completo
        abrirModalPedidoCompleto(pizza, tamanho) {
            console.log('Abrindo modal de pedido completo', pizza, tamanho);
            
            // Resetar modal
            this.modalPedido = {
                tipoPizza: 'inteira',
                sabor1: pizza,
                sabor1Id: pizza.id,
                sabor2: null,
                sabor2Id: null,
                tamanhoSelecionado: tamanho,
                tamanhoSelecionadoId: tamanho.id,
                tamanhos: pizza.tamanhos || [],
                borda: null,
                bebidas: {},
                observacoes: '',
                precoPizza: tamanho.preco,
                total: tamanho.preco
            };
            
            this.modalPedidoCompleto = true;
        },
        
        // Fechar modal
        fecharModalPedidoCompleto() {
            this.modalPedidoCompleto = false;
        },
        
        // Funções auxiliares de seleção
        selecionarSabor1ModalCompleto() {
            const pizzaSelecionada = this.produtosPorCategoria.pizzas.find(p => p.id == this.modalPedido.sabor1Id);
            if (pizzaSelecionada) {
                this.modalPedido.sabor1 = pizzaSelecionada;
                this.modalPedido.tamanhos = pizzaSelecionada.tamanhos || [];
                
                // Tentar manter o mesmo tamanho (P, M ou G) se disponível
                if (this.modalPedido.tamanhoSelecionado) {
                    const tamanhoNome = this.modalPedido.tamanhoSelecionado.nome;
                    const novoTamanho = pizzaSelecionada.tamanhos.find(t => t.nome === tamanhoNome);
                    
                    if (novoTamanho) {
                        // Mesmo tamanho disponível na nova pizza
                        this.modalPedido.tamanhoSelecionado = novoTamanho;
                        this.modalPedido.tamanhoSelecionadoId = novoTamanho.id;
                    } else {
                        // Tamanho não disponível, selecionar o primeiro
                        this.modalPedido.tamanhoSelecionado = pizzaSelecionada.tamanhos[0] || null;
                        this.modalPedido.tamanhoSelecionadoId = this.modalPedido.tamanhoSelecionado?.id || null;
                    }
                }
            }
            this.atualizarPrecoPedido();
        },
        
        selecionarSabor2ModalCompleto() {
            const pizzaSelecionada = this.produtosPorCategoria.pizzas.find(p => p.id == this.modalPedido.sabor2Id);
            if (pizzaSelecionada) {
                this.modalPedido.sabor2 = pizzaSelecionada;
            }
            this.atualizarPrecoPedido();
        },
        
        selecionarTamanhoModalCompleto() {
            const tamanhoSelecionado = this.modalPedido.tamanhos.find(t => t.id == this.modalPedido.tamanhoSelecionadoId);
            if (tamanhoSelecionado) {
                this.modalPedido.tamanhoSelecionado = tamanhoSelecionado;
                this.atualizarPrecoPedido();
            }
        },
        
        // Atualizar preço do pedido
        async atualizarPrecoPedido() {
            if (!this.modalPedido.tamanhoSelecionado) {
                this.modalPedido.precoPizza = 0;
                this.modalPedido.total = 0;
                return;
            }
            
            let precoPizza = 0;
            
            if (this.modalPedido.tipoPizza === 'inteira' && this.modalPedido.sabor1) {
                // Pizza inteira - preço simples
                const tamanho = this.modalPedido.sabor1.tamanhos?.find(t => t.id === this.modalPedido.tamanhoSelecionado.id);
                precoPizza = tamanho ? tamanho.preco : this.modalPedido.tamanhoSelecionado.preco;
            } else if (this.modalPedido.tipoPizza === 'meio-a-meio' && this.modalPedido.sabor1 && this.modalPedido.sabor2) {
                // Pizza meio a meio - calcular preço
                try {
                    this.calculandoPreco = true;
                    const response = await fetch('/api/pedidos/meio-a-meio/calcular-preco/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this.getCSRFToken()
                        },
                        body: JSON.stringify({
                            sabor_1_id: this.modalPedido.sabor1.id,
                            sabor_2_id: this.modalPedido.sabor2.id,
                            tamanho_id: this.modalPedido.tamanhoSelecionado.id,
                            regra_preco: 'mais_caro'
                        })
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        precoPizza = data.preco_final;
                    }
                } catch (error) {
                    console.error('Erro ao calcular preço:', error);
                    // Fallback: usar o maior preço
                    const preco1 = this.modalPedido.sabor1.tamanhos?.find(t => t.id === this.modalPedido.tamanhoSelecionado.id)?.preco || 0;
                    const preco2 = this.modalPedido.sabor2.tamanhos?.find(t => t.id === this.modalPedido.tamanhoSelecionado.id)?.preco || 0;
                    precoPizza = Math.max(preco1, preco2);
                } finally {
                    this.calculandoPreco = false;
                }
            }
            
            this.modalPedido.precoPizza = precoPizza;
            
            // Calcular total
            let total = precoPizza;
            
            // Adicionar borda
            if (this.modalPedido.borda) {
                total += this.modalPedido.borda.preco_unitario;
            }
            
            // Adicionar bebidas
            for (const [bebidaId, quantidade] of Object.entries(this.modalPedido.bebidas)) {
                if (quantidade > 0) {
                    const bebida = this.produtosPorCategoria.bebidas.find(b => b.id == bebidaId);
                    if (bebida) {
                        total += bebida.preco_unitario * quantidade;
                    }
                }
            }
            
            this.modalPedido.total = total;
        },
        
        // Controles de quantidade de bebida
        aumentarQuantidadeBebida(bebida) {
            if (!this.modalPedido.bebidas[bebida.id]) {
                this.modalPedido.bebidas[bebida.id] = 0;
            }
            this.modalPedido.bebidas[bebida.id]++;
            this.atualizarPrecoPedido();
        },
        
        diminuirQuantidadeBebida(bebida) {
            if (this.modalPedido.bebidas[bebida.id] && this.modalPedido.bebidas[bebida.id] > 0) {
                this.modalPedido.bebidas[bebida.id]--;
                if (this.modalPedido.bebidas[bebida.id] === 0) {
                    delete this.modalPedido.bebidas[bebida.id];
                }
                this.atualizarPrecoPedido();
            }
        },
        
        // Adicionar pedido completo ao carrinho
        adicionarPedidoCompletoAoCarrinho() {
            if (!this.modalPedido.sabor1 || !this.modalPedido.tamanhoSelecionado) {
                return;
            }
            
            if (this.modalPedido.tipoPizza === 'meio-a-meio' && !this.modalPedido.sabor2) {
                return;
            }
            
            // Adicionar pizza ao carrinho
            let pizzaItem;
            
            if (this.modalPedido.tipoPizza === 'inteira') {
                pizzaItem = {
                    id: Date.now(),
                    produto_id: this.modalPedido.sabor1.id,
                    nome: this.modalPedido.sabor1.nome,
                    tamanho: this.modalPedido.tamanhoSelecionado.nome,
                    preco: this.modalPedido.precoPizza,
                    quantidade: 1,
                    tipo: 'pizza',
                    observacoes: this.modalPedido.observacoes
                };
            } else {
                pizzaItem = {
                    id: Date.now(),
                    tipo: 'meio_a_meio',
                    nome: `Meio a Meio: ${this.modalPedido.sabor1.nome} + ${this.modalPedido.sabor2.nome}`,
                    tamanho: this.modalPedido.tamanhoSelecionado.nome,
                    preco: this.modalPedido.precoPizza,
                    quantidade: 1,
                    observacoes: this.modalPedido.observacoes,
                    meio_a_meio_data: {
                        is_meio_a_meio: true,
                        sabor_1: {
                            id: this.modalPedido.sabor1.id,
                            nome: this.modalPedido.sabor1.nome
                        },
                        sabor_2: {
                            id: this.modalPedido.sabor2.id,
                            nome: this.modalPedido.sabor2.nome
                        },
                        tamanho: this.modalPedido.tamanhoSelecionado.nome,
                        tamanho_id: this.modalPedido.tamanhoSelecionado.id,
                        regra_preco: 'mais_caro'
                    }
                };
            }
            
            // Adicionar borda se selecionada
            if (this.modalPedido.borda) {
                pizzaItem.nome += ` + Borda ${this.modalPedido.borda.nome}`;
                pizzaItem.preco += this.modalPedido.borda.preco_unitario;
                pizzaItem.borda = {
                    id: this.modalPedido.borda.id,
                    nome: this.modalPedido.borda.nome,
                    preco: this.modalPedido.borda.preco_unitario
                };
            }
            
            this.carrinho.push(pizzaItem);
            
            // Adicionar bebidas ao carrinho
            for (const [bebidaId, quantidade] of Object.entries(this.modalPedido.bebidas)) {
                if (quantidade > 0) {
                    const bebida = this.produtosPorCategoria.bebidas.find(b => b.id == bebidaId);
                    if (bebida) {
                        const bebidaItem = {
                            id: Date.now() + parseInt(bebidaId),
                            produto_id: bebida.id,
                            nome: bebida.nome,
                            preco: bebida.preco_unitario,
                            quantidade: quantidade,
                            tipo: 'bebida'
                        };
                        this.carrinho.push(bebidaItem);
                    }
                }
            }
            
            this.calcularTotal();
            this.fecharModalPedidoCompleto();
            this.mostrarFeedback('Pedido adicionado ao carrinho!');
        },
        
        // === FUNÇÕES DO MODAL DADOS CLIENTE ===
        
        // Abrir modal de dados do cliente
        abrirModalDadosCliente() {
            if (this.carrinho.length === 0) {
                this.mostrarFeedback('Adicione itens ao pedido primeiro!');
                return;
            }
            this.modalDadosCliente = true;
        },
        
        // Fechar modal
        fecharModalDadosCliente() {
            this.modalDadosCliente = false;
        },
        
        // Adicionar mais pizzas
        adicionarMaisPizzas() {
            // Scroll para o topo da página
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },
        
        // Formatar telefone
        formatarTelefone(event) {
            let value = event.target.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
            }
            event.target.value = value;
            this.cliente.telefone = value;
        },
        
        // Finalizar pedido
        async finalizarPedido() {
            if (!this.cliente.nome || !this.cliente.telefone) {
                this.mostrarFeedback('Preencha todos os campos obrigatórios!');
                return;
            }
            
            if (this.tipoPedido === 'delivery' && !this.cliente.endereco_simples) {
                this.mostrarFeedback('Informe o endereço de entrega!');
                return;
            }
            
            this.processandoPedido = true;
            
            try {
                // Preparar dados do pedido
                const pedidoData = {
                    tipo: this.tipoPedido,
                    forma_pagamento: this.formaPagamento,
                    troco_para: this.formaPagamento === 'dinheiro' ? this.trocoPara : null,
                    observacoes: this.observacoes,
                    cliente: this.cliente,
                    itens: this.carrinho.map(item => ({
                        produto_id: item.produto_id,
                        quantidade: item.quantidade,
                        preco_unitario: item.preco,
                        observacoes: item.observacoes || '',
                        // Dados adicionais para meio a meio
                        ...(item.meio_a_meio_data ? { meio_a_meio_data: item.meio_a_meio_data } : {}),
                        // Dados da borda
                        ...(item.borda ? { borda: item.borda } : {})
                    })),
                    taxa_entrega: this.tipoPedido === 'delivery' ? this.taxaEntrega : 0,
                    total: this.total
                };
                
                console.log('Enviando pedido:', pedidoData);
                
                const response = await fetch('/api/pedidos/criar_pedido_seguro/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: JSON.stringify(pedidoData)
                });
                
                const result = await response.json();
                
                if (response.ok && result.pedido_id) {
                    this.mostrarFeedback('Pedido criado com sucesso!');
                    // Limpar carrinho
                    this.carrinho = [];
                    this.calcularTotal();
                    // Fechar modais
                    this.fecharModalDadosCliente();
                    // Redirecionar ou mostrar confirmação
                    window.location.href = `/pedidos/${result.pedido_id}/confirmacao/`;
                } else {
                    throw new Error(result.erro || 'Erro ao criar pedido');
                }
            } catch (error) {
                console.error('Erro ao finalizar pedido:', error);
                this.mostrarFeedback('Erro ao criar pedido. Tente novamente.');
            } finally {
                this.processandoPedido = false;
            }
        },

        // Helper para CSRF token
        getCSRFToken() {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'csrftoken') {
                    return value;
                }
            }
            return '';
        }
    };
}

// Adicionar classe para prevenir scroll quando modal estiver aberto
document.addEventListener('alpine:init', () => {
    Alpine.data('pedidoForm', pedidoForm);
});