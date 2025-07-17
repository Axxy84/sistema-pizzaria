// Componente Alpine.js para o novo sistema unificado de pedidos
function pedidoUnificado() {
    return {
        // Estados principais
        tipoPizza: 'inteira',
        buscaPizza: '',
        
        // Pizza Inteira
        pizzaSelecionada: null,
        tamanhoSelecionado: null,
        
        // Pizza Meio a Meio
        sabor1: null,
        sabor2: null,
        
        // Complementos
        bordaSelecionada: '',
        bebidasSelecionadas: [],
        observacoes: '',
        
        // Carrinho
        carrinho: [],
        
        // Dados dinâmicos
        pizzas: [],
        bordas: [],
        bebidas: [],
        
        // Computed
        get pizzasFiltradas() {
            if (!this.buscaPizza) return this.pizzas;
            
            const busca = this.buscaPizza.toLowerCase();
            return this.pizzas.filter(pizza => 
                pizza.nome.toLowerCase().includes(busca) ||
                pizza.descricao.toLowerCase().includes(busca)
            );
        },
        
        // Métodos - Pizza Inteira
        selecionarPizza(pizza, tamanho) {
            this.pizzaSelecionada = pizza;
            this.tamanhoSelecionado = tamanho;
            
            // Scroll suave para mostrar as opções extras
            setTimeout(() => {
                document.querySelector('[x-show="pizzaSelecionada || (sabor1 && sabor2 && tamanhoSelecionado)"]')
                    ?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }, 100);
        },
        
        // Métodos - Meio a Meio
        selecionarSabor1(pizza) {
            this.sabor1 = pizza;
            if (this.sabor2 && this.sabor2.id === pizza.id) {
                this.sabor2 = null;
            }
        },
        
        selecionarSabor2(pizza) {
            this.sabor2 = pizza;
        },
        
        selecionarTamanhoMeioAMeio(tamanho) {
            this.tamanhoSelecionado = tamanho;
        },
        
        calcularPrecoMeioAMeio(tamanho) {
            if (!this.sabor1 || !this.sabor2) return 0;
            
            // Pega o preço do tamanho para cada sabor
            const precoSabor1 = this.sabor1.tamanhos.find(t => t.nome === tamanho.nome)?.preco || 0;
            const precoSabor2 = this.sabor2.tamanhos.find(t => t.nome === tamanho.nome)?.preco || 0;
            
            // Usa o preço mais caro (regra padrão)
            return Math.max(precoSabor1, precoSabor2);
        },
        
        // Métodos - Bebidas
        toggleBebida(bebida) {
            const index = this.bebidasSelecionadas.findIndex(b => b.id === bebida.id);
            if (index === -1) {
                this.bebidasSelecionadas.push({ ...bebida, quantidade: 1 });
            } else {
                this.bebidasSelecionadas.splice(index, 1);
            }
        },
        
        aumentarQuantidadeBebida(bebida) {
            const item = this.bebidasSelecionadas.find(b => b.id === bebida.id);
            if (item) item.quantidade++;
        },
        
        diminuirQuantidadeBebida(bebida) {
            const item = this.bebidasSelecionadas.find(b => b.id === bebida.id);
            if (item) {
                if (item.quantidade > 1) {
                    item.quantidade--;
                } else {
                    this.toggleBebida(bebida);
                }
            }
        },
        
        // Cálculos
        calcularTotalItem() {
            let total = 0;
            
            // Preço da pizza
            if (this.tipoPizza === 'inteira' && this.tamanhoSelecionado) {
                total += this.tamanhoSelecionado.preco;
            } else if (this.tipoPizza === 'meio-a-meio' && this.tamanhoSelecionado) {
                total += this.calcularPrecoMeioAMeio(this.tamanhoSelecionado);
            }
            
            // Preço da borda
            if (this.bordaSelecionada) {
                const borda = this.bordas.find(b => b.id == this.bordaSelecionada);
                if (borda) total += borda.preco;
            }
            
            // Preço das bebidas
            this.bebidasSelecionadas.forEach(bebida => {
                total += bebida.preco * bebida.quantidade;
            });
            
            return total;
        },
        
        // Carrinho
        adicionarAoCarrinho() {
            // Validações
            if (this.tipoPizza === 'inteira') {
                if (!this.pizzaSelecionada || !this.tamanhoSelecionado) {
                    alert('Selecione uma pizza e tamanho!');
                    return;
                }
            } else {
                if (!this.sabor1 || !this.sabor2 || !this.tamanhoSelecionado) {
                    alert('Selecione os dois sabores e o tamanho!');
                    return;
                }
            }
            
            // Monta o item do carrinho
            let item = {
                tipo: 'pizza',
                nome: '',
                detalhes: '',
                preco: this.calcularTotalItem(),
                dados: {
                    tipoPizza: this.tipoPizza,
                    observacoes: this.observacoes
                }
            };
            
            // Nome e detalhes
            if (this.tipoPizza === 'inteira') {
                item.nome = `Pizza ${this.pizzaSelecionada.nome}`;
                item.detalhes = `${this.tamanhoSelecionado.nome === 'P' ? 'Pequena' : 
                                   this.tamanhoSelecionado.nome === 'M' ? 'Média' : 'Grande'}`;
                item.dados.pizza = this.pizzaSelecionada;
                item.dados.tamanho = this.tamanhoSelecionado;
            } else {
                item.nome = `Pizza ${this.sabor1.nome} / ${this.sabor2.nome}`;
                item.detalhes = `${this.tamanhoSelecionado.nome === 'P' ? 'Pequena' : 
                                   this.tamanhoSelecionado.nome === 'M' ? 'Média' : 'Grande'} - Meio a Meio`;
                item.dados.sabor1 = this.sabor1;
                item.dados.sabor2 = this.sabor2;
                item.dados.tamanho = this.tamanhoSelecionado;
            }
            
            // Adiciona borda se selecionada
            if (this.bordaSelecionada) {
                const borda = this.bordas.find(b => b.id == this.bordaSelecionada);
                item.detalhes += ` + Borda ${borda.nome}`;
                item.dados.borda = borda;
            }
            
            // Adiciona bebidas
            if (this.bebidasSelecionadas.length > 0) {
                item.dados.bebidas = [...this.bebidasSelecionadas];
                const nomesBebidas = this.bebidasSelecionadas.map(b => `${b.quantidade}x ${b.nome}`).join(', ');
                item.detalhes += ` + ${nomesBebidas}`;
            }
            
            // Adiciona ao carrinho
            this.carrinho.push(item);
            
            // Limpa seleções
            this.limparSelecoes();
            
            // Feedback visual
            this.mostrarNotificacao('Item adicionado ao carrinho!');
            
            // Scroll para o carrinho
            document.querySelector('[x-text="carrinho.length"]')
                ?.closest('.bg-white')
                ?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        },
        
        removerDoCarrinho(index) {
            this.carrinho.splice(index, 1);
        },
        
        calcularTotalCarrinho() {
            return this.carrinho.reduce((total, item) => total + item.preco, 0);
        },
        
        // Limpar seleções
        limparSelecoes() {
            this.pizzaSelecionada = null;
            this.tamanhoSelecionado = null;
            this.sabor1 = null;
            this.sabor2 = null;
            this.bordaSelecionada = '';
            this.bebidasSelecionadas = [];
            this.observacoes = '';
        },
        
        // Notificação
        mostrarNotificacao(mensagem) {
            // Cria notificação temporária
            const notif = document.createElement('div');
            notif.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
            notif.textContent = mensagem;
            document.body.appendChild(notif);
            
            // Remove após 3 segundos
            setTimeout(() => {
                notif.remove();
            }, 3000);
        },
        
        // Finalizar pedido
        finalizarPedido() {
            if (this.carrinho.length === 0) {
                alert('Carrinho vazio!');
                return;
            }
            
            // Aqui você redirecionaria para a tela de finalização
            // ou abriria um modal com dados do cliente
            console.log('Pedido:', this.carrinho);
            console.log('Total:', this.calcularTotalCarrinho());
            
            alert(`Pedido com ${this.carrinho.length} itens - Total: R$ ${this.calcularTotalCarrinho().toFixed(2)}`);
        },
        
        // Filtros
        filtrarPizzas() {
            // Força reatividade do Alpine
            this.pizzas = [...this.pizzas];
        },
        
        // Init
        init() {
            console.log('Sistema de pedidos unificado iniciado!');
            
            // Carrega dados reais da API se disponível
            this.carregarDados();
        },
        
        // Carregar dados da API
        async carregarDados() {
            try {
                // Buscar produtos organizados por categoria
                const response = await fetch('/api/produtos/produtos/para_pedido/');
                const data = await response.json();
                
                if (data.produtos_por_categoria) {
                    // Processar pizzas
                    this.pizzas = data.produtos_por_categoria.pizzas?.map(pizza => ({
                        id: pizza.id,
                        nome: pizza.nome,
                        descricao: pizza.descricao,
                        tamanhos: pizza.tamanhos.map(t => ({
                            id: t.id,
                            nome: t.nome,
                            preco: parseFloat(t.preco)
                        }))
                    })) || [];
                    
                    // Processar bordas
                    this.bordas = data.produtos_por_categoria.bordas?.map(borda => ({
                        id: borda.id,
                        nome: borda.nome,
                        preco: parseFloat(borda.preco_unico || borda.tamanhos[0]?.preco || 0)
                    })) || [];
                    
                    // Processar bebidas
                    this.bebidas = data.produtos_por_categoria.bebidas?.map(bebida => ({
                        id: bebida.id,
                        nome: bebida.nome,
                        preco: parseFloat(bebida.preco_unico || bebida.tamanhos[0]?.preco || 0)
                    })) || [];
                    
                    console.log('Dados carregados:', {
                        pizzas: this.pizzas.length,
                        bordas: this.bordas.length,
                        bebidas: this.bebidas.length
                    });
                }
            } catch (error) {
                console.error('Erro ao carregar dados:', error);
                // Fallback para dados de exemplo se a API falhar
                this.carregarDadosExemplo();
            }
        },
        
        // Dados de exemplo como fallback
        carregarDadosExemplo() {
            this.pizzas = [
                {
                    id: 1,
                    nome: 'MARGHERITA',
                    descricao: 'Molho de tomate, mussarela de búfala, manjericão fresco',
                    tamanhos: [
                        { id: 1, nome: 'P', preco: 35 },
                        { id: 2, nome: 'M', preco: 45 },
                        { id: 3, nome: 'G', preco: 55 }
                    ]
                },
                {
                    id: 2,
                    nome: 'CALABRESA',
                    descricao: 'Molho de tomate, mussarela, calabresa, cebola',
                    tamanhos: [
                        { id: 4, nome: 'P', preco: 30 },
                        { id: 5, nome: 'M', preco: 40 },
                        { id: 6, nome: 'G', preco: 50 }
                    ]
                }
            ];
            
            this.bordas = [
                { id: 1, nome: 'Catupiry', preco: 8 },
                { id: 2, nome: 'Cheddar', preco: 8 }
            ];
            
            this.bebidas = [
                { id: 1, nome: 'Coca-Cola 2L', preco: 12.00 },
                { id: 2, nome: 'Guaraná 2L', preco: 10.00 }
            ];
        }
    }
}