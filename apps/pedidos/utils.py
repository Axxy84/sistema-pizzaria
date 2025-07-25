"""
Utilitários para melhorar a integração com Supabase
Inclui tratamento de erros, validações e helpers
"""

from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.db import transaction
from services.supabase_client import get_supabase_client
import logging

logger = logging.getLogger(__name__)

class PedidoValidator:
    """Classe para validar dados de pedidos"""
    
    @staticmethod
    def validar_dados_cliente(dados_cliente):
        """Valida dados do cliente"""
        erros = []
        
        if not dados_cliente.get('nome', '').strip():
            erros.append("Nome do cliente é obrigatório")
        
        telefone = dados_cliente.get('telefone', '').strip()
        if not telefone:
            erros.append("Telefone do cliente é obrigatório")
        elif len(telefone) < 10:
            erros.append("Telefone deve ter pelo menos 10 dígitos")
        
        email = dados_cliente.get('email', '').strip()
        if email and '@' not in email:
            erros.append("Email inválido")
        
        return erros
    
    @staticmethod
    def validar_itens_pedido(itens):
        """Valida itens do pedido"""
        erros = []
        
        if not itens or len(itens) == 0:
            erros.append("Pedido deve ter pelo menos um item")
            return erros
        
        for i, item in enumerate(itens):
            item_prefix = f"Item {i+1}: "
            
            # Para pizzas meio a meio, verificar sabores; para produtos normais, verificar produto_id
            if item.get('meio_a_meio'):
                if not item.get('sabor1_id') or not item.get('sabor2_id'):
                    erros.append(f"{item_prefix}pizza meio a meio deve ter sabor1_id e sabor2_id")
            else:
                if not item.get('produto_id'):
                    erros.append(f"{item_prefix}produto_id é obrigatório")
            
            quantidade = item.get('quantidade', 0)
            if not isinstance(quantidade, int) or quantidade <= 0:
                erros.append(f"{item_prefix}quantidade deve ser um número inteiro positivo")
            
            try:
                preco = Decimal(str(item.get('preco_unitario', 0)))
                if preco <= 0:
                    erros.append(f"{item_prefix}preço deve ser maior que zero")
            except (InvalidOperation, ValueError):
                erros.append(f"{item_prefix}preço inválido")
        
        return erros
    
    @staticmethod
    def validar_pedido_completo(dados_pedido):
        """Valida pedido completo"""
        erros = []
        
        # Validar cliente
        if 'cliente' in dados_pedido:
            erros.extend(PedidoValidator.validar_dados_cliente(dados_pedido['cliente']))
        else:
            erros.append("Dados do cliente são obrigatórios")
        
        # Validar itens
        if 'itens' in dados_pedido:
            erros.extend(PedidoValidator.validar_itens_pedido(dados_pedido['itens']))
        else:
            erros.append("Itens do pedido são obrigatórios")
        
        # Validar tipo de pedido
        tipo = dados_pedido.get('tipo', '')
        if tipo not in ['delivery', 'balcao', 'mesa']:
            erros.append("Tipo de pedido deve ser 'delivery', 'balcao' ou 'mesa'")
        
        # Validar forma de pagamento
        forma_pagamento = dados_pedido.get('forma_pagamento', '')
        if forma_pagamento not in ['dinheiro', 'pix', 'cartao_credito', 'cartao_debito', 'vale_refeicao']:
            erros.append("Forma de pagamento inválida")
        
        return erros

class SupabaseErrorHandler:
    """Classe para tratar erros específicos do Supabase"""
    
    @staticmethod
    def tratar_erro_supabase(erro):
        """Converte erros do Supabase em mensagens amigáveis"""
        erro_str = str(erro).lower()
        
        if 'connection' in erro_str or 'timeout' in erro_str:
            return "Erro de conexão com o banco de dados. Tente novamente."
        
        if 'unique constraint' in erro_str or 'duplicate key' in erro_str:
            return "Já existe um registro com essas informações."
        
        if 'foreign key' in erro_str:
            return "Erro de integridade dos dados. Verifique as informações."
        
        if 'not null constraint' in erro_str:
            return "Campos obrigatórios não foram preenchidos."
        
        if 'permission denied' in erro_str or 'rls' in erro_str:
            return "Sem permissão para realizar esta operação."
        
        return "Erro interno do sistema. Contate o suporte."

class PedidoSupabaseManager:
    """Gerenciador para operações de pedido com Supabase"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def verificar_conectividade(self):
        """Verifica se a conexão com Supabase está funcionando"""
        try:
            result = self.supabase.table('produtos_produto').select('count').limit(1).execute()
            return True, "Conectado ao Supabase"
        except Exception as e:
            logger.error(f"Erro de conectividade Supabase: {e}")
            return False, SupabaseErrorHandler.tratar_erro_supabase(e)
    
    def buscar_produto_seguro(self, produto_id):
        """Busca produto com tratamento de erros"""
        try:
            result = self.supabase.table('produtos_produto').select('*').eq('id', produto_id).eq('ativo', True).execute()
            
            if not result.data:
                return None, "Produto não encontrado ou inativo"
            
            return result.data[0], None
        except Exception as e:
            logger.error(f"Erro ao buscar produto {produto_id}: {e}")
            return None, SupabaseErrorHandler.tratar_erro_supabase(e)
    
    def criar_pedido_seguro(self, dados_pedido):
        """Cria pedido com validações e tratamento de erros"""
        try:
            # Validar dados
            erros = PedidoValidator.validar_pedido_completo(dados_pedido)
            if erros:
                return None, erros
            
            # Verificar conectividade
            conectado, erro_conn = self.verificar_conectividade()
            if not conectado:
                return None, [erro_conn]
            
            # Criar pedido com transação simulada
            with transaction.atomic():
                from apps.clientes.models import Cliente
                from apps.pedidos.models import Pedido, ItemPedido
                from apps.produtos.models import Produto, ProdutoPreco
                                
                # Criar ou buscar cliente
                dados_cliente = dados_pedido['cliente']
                cliente, created = Cliente.objects.get_or_create(
                    telefone=dados_cliente['telefone'],
                    defaults={
                        'nome': dados_cliente['nome'],
                        'email': dados_cliente.get('email', '')
                    }
                )
                
                # Buscar usuário para o pedido
                usuario = get_user_model().objects.first()
                if not usuario:
                    return None, ["Nenhum usuário encontrado no sistema"]
                
                # Calcular totais
                subtotal = Decimal('0')
                for item in dados_pedido['itens']:
                    quantidade = item['quantidade']
                    preco = Decimal(str(item['preco_unitario']))
                    subtotal += quantidade * preco
                
                taxa_entrega = Decimal('0')
                if dados_pedido.get('tipo') == 'delivery':
                    taxa_entrega = Decimal('5.00')  # Taxa padrão
                
                total = subtotal + taxa_entrega
                
                # Criar pedido
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    usuario=usuario,
                    tipo=dados_pedido['tipo'],
                    forma_pagamento=dados_pedido['forma_pagamento'],
                    subtotal=subtotal,
                    taxa_entrega=taxa_entrega,
                    total=total,
                    observacoes=dados_pedido.get('observacoes', '')
                )
                
                # Adicionar itens
                itens_criados = []
                for item in dados_pedido['itens']:
                    if item.get('meio_a_meio'):
                        # Processar pizza meio a meio
                        sabor1_id = item.get('sabor1_id')
                        sabor2_id = item.get('sabor2_id')
                        
                        if not sabor1_id or not sabor2_id:
                            raise ValidationError("Pizza meio a meio deve ter dois sabores válidos")
                        
                        # Buscar produtos dos sabores
                        produto1 = Produto.objects.filter(id=sabor1_id, ativo=True).first()
                        produto2 = Produto.objects.filter(id=sabor2_id, ativo=True).first()
                        
                        if not produto1:
                            raise ValidationError(f"Produto sabor 1 (ID: {sabor1_id}) não encontrado")
                        if not produto2:
                            raise ValidationError(f"Produto sabor 2 (ID: {sabor2_id}) não encontrado")
                        
                        # Para pizza meio a meio, usar o primeiro produto como base
                        produto_preco = ProdutoPreco.objects.filter(produto=produto1).first()
                        if not produto_preco:
                            # Criar ProdutoPreco se não existir
                            from apps.produtos.models import Tamanho
                            tamanho_padrao = Tamanho.objects.first()
                            if not tamanho_padrao:
                                raise ValidationError("Nenhum tamanho cadastrado no sistema")
                            
                            produto_preco = ProdutoPreco.objects.create(
                                produto=produto1,
                                tamanho=tamanho_padrao,
                                preco=Decimal(str(item['preco_unitario']))
                            )
                        
                        # Criar item com observações especiais para meio a meio
                        observacoes_completas = f"MEIO A MEIO: {produto1.nome} + {produto2.nome}"
                        if item.get('observacoes'):
                            observacoes_completas += f" | {item['observacoes']}"
                        
                        item_pedido = ItemPedido.objects.create(
                            pedido=pedido,
                            produto_preco=produto_preco,
                            quantidade=item['quantidade'],
                            preco_unitario=Decimal(str(item['preco_unitario'])),
                            subtotal=Decimal(str(item['preco_unitario'])) * item['quantidade'],
                            observacoes=observacoes_completas
                        )
                        itens_criados.append(item_pedido)
                        
                    else:
                        # Processar produto normal
                        produto = Produto.objects.filter(id=item['produto_id'], ativo=True).first()
                        if not produto:
                            raise ValidationError(f"Produto {item['produto_id']} não encontrado")
                        
                        # Buscar preço do produto
                        produto_preco = ProdutoPreco.objects.filter(produto=produto).first()
                        if not produto_preco:
                            # Se não tem preço específico, criar um ProdutoPreco
                            if not produto.preco_unitario:
                                raise ValidationError(f"Produto {produto.nome} sem preço configurado")
                            
                            # Criar ProdutoPreco com base no preço unitário do produto
                            # Buscar tamanho padrão (primeiro tamanho disponível)
                            from apps.produtos.models import Tamanho
                            tamanho_padrao = Tamanho.objects.first()
                            if not tamanho_padrao:
                                raise ValidationError("Nenhum tamanho cadastrado no sistema")
                            
                            produto_preco = ProdutoPreco.objects.create(
                                produto=produto,
                                tamanho=tamanho_padrao,
                                preco=produto.preco_unitario
                            )
                        
                        item_pedido = ItemPedido.objects.create(
                            pedido=pedido,
                            produto_preco=produto_preco,
                            quantidade=item['quantidade'],
                            preco_unitario=Decimal(str(item['preco_unitario'])),
                            subtotal=Decimal(str(item['preco_unitario'])) * item['quantidade'],
                            observacoes=item.get('observacoes', '')
                        )
                        itens_criados.append(item_pedido)
                
                logger.info(f"Pedido {pedido.numero} criado com sucesso: {len(itens_criados)} itens, total R$ {total}")
                
                return {
                    'pedido': pedido,
                    'itens': itens_criados,
                    'total': total
                }, None
                
        except ValidationError as e:
            logger.error(f"Erro de validação: {e}")
            return None, [str(e)]
        except Exception as e:
            logger.error(f"Erro ao criar pedido: {e}")
            logger.error(f"Tipo do erro: {type(e)}")
            logger.error(f"Dados que causaram erro: {dados_pedido}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            return None, [f"Erro interno detalhado: {str(e)}"]
    
    def criar_pedido_completo(self, dados_pedido):
        """Cria pedido completo com cliente, endereço e itens"""
        try:
            # Validações iniciais
            erros = []
            
            # Validar estrutura dos dados
            if not isinstance(dados_pedido, dict):
                return {'status': 'error', 'message': 'Dados do pedido inválidos'}
            
            tipo = dados_pedido.get('tipo', 'balcao')
            cliente_data = dados_pedido.get('cliente', {})
            mesa_data = dados_pedido.get('mesa', {})
            endereco_data = dados_pedido.get('endereco', {})
            pagamento_data = dados_pedido.get('pagamento', {})
            itens = dados_pedido.get('itens', [])
            observacoes = dados_pedido.get('observacoes', '')
            
            # Validações específicas
            if not cliente_data.get('nome'):
                erros.append('Nome do cliente é obrigatório')
            
            if not cliente_data.get('telefone'):
                erros.append('Telefone do cliente é obrigatório')
            
            if not itens:
                erros.append('É necessário adicionar pelo menos um item')
            
            if not pagamento_data.get('forma'):
                erros.append('Forma de pagamento é obrigatória')
            
            if tipo == 'mesa' and not mesa_data.get('numero'):
                erros.append('Número da mesa é obrigatório')
            
            if tipo == 'delivery':
                if not endereco_data.get('rua'):
                    erros.append('Rua é obrigatória para delivery')
                if not endereco_data.get('numero'):
                    erros.append('Número é obrigatório para delivery')
                if not endereco_data.get('bairro'):
                    erros.append('Bairro é obrigatório para delivery')
            
            if erros:
                return {'status': 'error', 'message': '; '.join(erros)}
            
            # Criar estrutura de dados para o método existente
            dados_para_criar = {
                'tipo': tipo,
                'cliente': cliente_data,
                'itens': itens,
                'forma_pagamento': pagamento_data.get('forma'),
                'observacoes': observacoes
            }
            
            # Usar método existente
            resultado, erro = self.criar_pedido_seguro(dados_para_criar)
            
            if erro:
                return {'status': 'error', 'message': '; '.join(erro)}
            
            # Sucesso
            pedido = resultado['pedido']
            return {
                'status': 'success',
                'pedido_id': pedido.id,
                'numero_pedido': pedido.numero,
                'total': float(resultado['total']),
                'message': 'Pedido criado com sucesso!'
            }
            
        except Exception as e:
            logger.error(f"Erro em criar_pedido_completo: {e}")
            return {'status': 'error', 'message': f'Erro interno: {str(e)}'}

class SupabaseHealthCheck:
    """Classe para monitorar saúde da integração"""
    
    @staticmethod
    def status_completo():
        """Retorna status completo da integração"""
        status = {
            'conectividade': False,
            'tabelas_acessiveis': [],
            'erros': [],
            'metricas': {}
        }
        
        try:
            supabase = get_supabase_client()
            
            # Testar tabelas principais
            tabelas_teste = [
                'produtos_produto',
                'produtos_categoria', 
                'clientes_cliente',
                'pedidos_pedido',
                'pedidos_itempedido'
            ]
            
            for tabela in tabelas_teste:
                try:
                    result = supabase.table(tabela).select('count').limit(1).execute()
                    status['tabelas_acessiveis'].append(tabela)
                except Exception as e:
                    status['erros'].append(f"Erro em {tabela}: {e}")
            
            status['conectividade'] = len(status['tabelas_acessiveis']) > 0
            
            # Métricas básicas
            if status['conectividade']:
                try:
                    produtos = supabase.table('produtos_produto').select('count').execute()
                    pedidos = supabase.table('pedidos_pedido').select('count').execute()
                    clientes = supabase.table('clientes_cliente').select('count').execute()
                    
                    status['metricas'] = {
                        'produtos_cadastrados': len(produtos.data) if produtos.data else 0,
                        'pedidos_total': len(pedidos.data) if pedidos.data else 0,
                        'clientes_cadastrados': len(clientes.data) if clientes.data else 0
                    }
                except Exception as e:
                    status['erros'].append(f"Erro ao buscar métricas: {e}")
            
        except Exception as e:
            status['erros'].append(f"Erro geral: {e}")
        
        return status