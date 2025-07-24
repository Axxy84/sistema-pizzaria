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
try:
    from .impressao_escpos import imprimir_pedido_escpos
    ESCPOS_DISPONIVEL = True
except ImportError:
    ESCPOS_DISPONIVEL = False
import json
import subprocess
import os

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
    Imprime a comanda na impressora térmica com múltiplos métodos
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Pegar nome da impressora do POST ou usar padrão
    data = json.loads(request.body) if request.body else {}
    impressora = data.get('impressora', None)
    
    # Gerar texto da comanda
    comanda_texto = gerar_comanda_texto_puro(pedido)
    
    # Salvar em arquivo temporário
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='cp850', errors='replace') as f:
        f.write(comanda_texto)
        arquivo_temp = f.name
    
    sucesso = False
    mensagens_erro = []
    
    try:
        # Tentar primeiro com ESC/POS se disponível
        if ESCPOS_DISPONIVEL and data.get('usar_escpos', False):
            try:
                sucesso, msg = imprimir_pedido_escpos(pedido)
                if not sucesso:
                    mensagens_erro.append(f"ESC/POS: {msg}")
            except Exception as e:
                mensagens_erro.append(f"ESC/POS: {str(e)}")
        
        # Se não funcionou, usar métodos anteriores
        if not sucesso:
            # Método 1: Comando PRINT do Windows
            if impressora:
                cmd = f'print /D:"{impressora}" "{arquivo_temp}"'
            else:
                cmd = f'print "{arquivo_temp}"'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                sucesso = True
            else:
                mensagens_erro.append(f"PRINT: {result.stderr or 'Falhou'}")
        
        # Se não funcionou, tentar método 2: Notepad silencioso
        if not sucesso:
            cmd_notepad = f'notepad /p "{arquivo_temp}"'
            result2 = subprocess.run(cmd_notepad, shell=True, capture_output=True, text=True, timeout=10)
            if result2.returncode == 0:
                sucesso = True
            else:
                mensagens_erro.append(f"NOTEPAD: {result2.stderr or 'Falhou'}")
        
        # Método 3: Copiar direto para porta (se soubermos qual é)
        if not sucesso and not impressora:
            # Tentar descobrir a porta da impressora
            cmd_porta = 'wmic printer where "name like \'%KNUP%\'" get portname /value'
            result_porta = subprocess.run(cmd_porta, shell=True, capture_output=True, text=True)
            
            if result_porta.stdout:
                for linha in result_porta.stdout.split('\n'):
                    if 'PortName=' in linha:
                        porta = linha.split('=')[1].strip()
                        if porta:
                            cmd_copy = f'copy "{arquivo_temp}" {porta}'
                            result3 = subprocess.run(cmd_copy, shell=True, capture_output=True, text=True)
                            if result3.returncode == 0:
                                sucesso = True
                                break
                            else:
                                mensagens_erro.append(f"COPY {porta}: Falhou")
        
        if sucesso:
            # Marcar como impresso
            pedido.comanda_impressa = True
            pedido.save(update_fields=['comanda_impressa'])
            
            return JsonResponse({
                'success': True,
                'message': 'Comanda enviada para impressora!'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Não foi possível imprimir. Erros: ' + ' | '.join(mensagens_erro),
                'sugestao': 'Tente baixar o arquivo .txt e imprimir manualmente'
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro ao imprimir: {str(e)}'
        }, status=500)
        
    finally:
        # Limpar arquivo temporário
        try:
            os.unlink(arquivo_temp)
        except:
            pass

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
    Imprime página de teste na impressora com múltiplos métodos
    """
    import tempfile
    import os
    from datetime import datetime
    
    # Texto de teste simples
    texto_teste = f"""========================================
         TESTE DE IMPRESSAO
========================================

Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Teste de caracteres:
- Numeros: 0123456789
- Letras: ABCDEFGHIJKLMNOPQRSTUVWXYZ
- Letras: abcdefghijklmnopqrstuvwxyz

Teste de acentos removidos:
- Original: acao voce maca Jose
- Este texto nao tem acentos

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
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='cp850', errors='replace') as f:
        f.write(texto_teste)
        arquivo_temp = f.name
    
    sucesso = False
    metodo_sucesso = ""
    
    try:
        # Tentar vários métodos
        
        # Método 1: PRINT
        if impressora:
            cmd = f'print /D:"{impressora}" "{arquivo_temp}"'
        else:
            cmd = f'print "{arquivo_temp}"'
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            sucesso = True
            metodo_sucesso = "PRINT"
        
        # Método 2: Notepad
        if not sucesso:
            subprocess.run(f'notepad /p "{arquivo_temp}"', shell=True, timeout=5)
            sucesso = True
            metodo_sucesso = "NOTEPAD"
        
        if sucesso:
            return JsonResponse({
                'success': True,
                'message': f'Teste enviado para impressora usando {metodo_sucesso}'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Não foi possível imprimir. Verifique se a impressora está configurada como padrão.'
            }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro: {str(e)}'
        }, status=500)
    
    finally:
        try:
            os.unlink(arquivo_temp)
        except:
            pass