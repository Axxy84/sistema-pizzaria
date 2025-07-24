"""
Views para impressão de comandas e pedidos
"""
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Pedido
from .utils_impressao import (
    gerar_comanda_texto_puro, 
    salvar_comanda_arquivo,
    imprimir_comanda_windows
)
import json

@require_http_methods(["GET"])
def visualizar_comanda(request, pedido_id):
    """
    Visualiza a comanda em formato texto antes de imprimir
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    comanda_texto = gerar_comanda_texto_puro(pedido)
    
    return render(request, 'pedidos/visualizar_comanda.html', {
        'pedido': pedido,
        'comanda_texto': comanda_texto
    })

@require_http_methods(["GET"])
def download_comanda(request, pedido_id):
    """
    Faz download da comanda em formato .txt
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    comanda_texto = gerar_comanda_texto_puro(pedido)
    
    response = HttpResponse(comanda_texto, content_type='text/plain; charset=cp850')
    response['Content-Disposition'] = f'attachment; filename="comanda_{pedido.numero}.txt"'
    
    return response

@require_http_methods(["POST"])
def imprimir_comanda(request, pedido_id):
    """
    Imprime a comanda na impressora térmica
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Pegar nome da impressora do POST ou usar padrão
    data = json.loads(request.body) if request.body else {}
    impressora = data.get('impressora', None)
    
    # Tentar imprimir
    sucesso, mensagem = imprimir_comanda_windows(pedido, impressora)
    
    if sucesso:
        # Marcar como impresso
        pedido.comanda_impressa = True
        pedido.save(update_fields=['comanda_impressa'])
        
        return JsonResponse({
            'success': True,
            'message': mensagem
        })
    else:
        return JsonResponse({
            'success': False,
            'error': mensagem
        }, status=400)

@require_http_methods(["GET"])
def testar_impressora(request):
    """
    Página para testar a impressora térmica
    """
    # Criar pedido de teste fake
    from datetime import datetime
    
    class PedidoTeste:
        numero = "TESTE001"
        criado_em = datetime.now()
        tipo = "balcao"
        total = 45.50
        subtotal = 45.50
        taxa_entrega = 0
        desconto = 0
        forma_pagamento = "dinheiro"
        observacoes = "Pedido de teste para verificar impressão"
        cliente = None
        mesa_numero = "Mesa 01"
        endereco_entrega = None
        precisa_troco = False
        troco_para = None
        comanda_impressa = False
        
        def get_tipo_display(self):
            return "Balcão"
        
        def get_forma_pagamento_display(self):
            return "Dinheiro"
        
        class Item:
            def __init__(self):
                self.quantidade = 1
                self.subtotal = 45.50
                self.observacoes = "Sem cebola"
                
                class ProdutoPreco:
                    class Produto:
                        nome = "Pizza Mussarela Grande"
                    
                    class Tamanho:
                        nome = "Grande"
                    
                    produto = Produto()
                    tamanho = Tamanho()
                
                self.produto_preco = ProdutoPreco()
        
        class ItemsManager:
            def all(self):
                return [PedidoTeste.Item()]
        
        itens = ItemsManager()
    
    pedido_teste = PedidoTeste()
    comanda_texto = gerar_comanda_texto_puro(pedido_teste)
    
    return render(request, 'pedidos/testar_impressora.html', {
        'comanda_texto': comanda_texto
    })

@require_http_methods(["POST"])
def imprimir_teste(request):
    """
    Imprime página de teste na impressora
    """
    import tempfile
    import os
    from datetime import datetime
    
    # Texto de teste simples
    texto_teste = f"""
========================================
         TESTE DE IMPRESSAO
========================================

Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Teste de caracteres:
- Numeros: 0123456789
- Letras: ABCDEFGHIJKLMNOPQRSTUVWXYZ
- Letras: abcdefghijklmnopqrstuvwxyz
- Especiais: !@#$%&*()_+-=[]{{}}|;:,.<>?

Teste de acentos removidos:
- Original: ação, você, maçã, José
- Limpo: acao, voce, maca, Jose

Teste de alinhamento:
Item                    Qtd   Valor
------------------------------------
Pizza Mussarela          1    45,00
Refrigerante             2     6,00
------------------------------------
TOTAL:                        51,00

========================================
      IMPRESSORA FUNCIONANDO OK!
========================================



"""
    
    # Pegar impressora do POST
    data = json.loads(request.body) if request.body else {}
    impressora = data.get('impressora', None)
    
    # Criar arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='cp850') as f:
        f.write(texto_teste)
        arquivo_temp = f.name
    
    try:
        import subprocess
        
        if impressora:
            cmd = f'print /D:"{impressora}" "{arquivo_temp}"'
        else:
            cmd = f'print "{arquivo_temp}"'
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return JsonResponse({
                'success': True,
                'message': 'Teste enviado para impressora'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': f'Erro ao imprimir: {result.stderr}'
            }, status=400)
    
    finally:
        try:
            os.unlink(arquivo_temp)
        except:
            pass