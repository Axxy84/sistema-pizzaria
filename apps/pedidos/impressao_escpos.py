"""
Módulo de impressão usando python-escpos
Suporte nativo para impressoras térmicas ESC/POS
"""
from escpos.printer import Serial, Usb, Dummy
import os
from .utils_impressao import limpar_texto_impressora, formatar_dinheiro
from decimal import Decimal

class ImpressoraTermica:
    def __init__(self):
        self.printer = None
        self.conectada = False
        
    def conectar_usb(self, vendor_id=None, product_id=None):
        """
        Conecta na impressora via USB
        IDs comuns para impressoras térmicas:
        - 0x04b8, 0x0202 (Epson)
        - 0x0483, 0x5720 (Generic)
        """
        try:
            if vendor_id and product_id:
                self.printer = Usb(vendor_id, product_id)
            else:
                # Tentar detectar automaticamente
                # IDs comuns para impressoras genéricas/KNUP
                ids_comuns = [
                    (0x0483, 0x5720),  # Generic
                    (0x04b8, 0x0202),  # Epson
                    (0x0416, 0x5011),  # Winbond
                    (0x0525, 0xa700),  # PLX
                    (0x1504, 0x0006),  # Generic 58mm
                    (0x1504, 0x0010),  # Generic 80mm
                ]
                
                for vid, pid in ids_comuns:
                    try:
                        self.printer = Usb(vid, pid)
                        self.conectada = True
                        return True
                    except:
                        continue
                        
                raise Exception("Nenhuma impressora USB encontrada")
                
            self.conectada = True
            return True
        except Exception as e:
            return False, str(e)
    
    def conectar_serial(self, porta='COM1', baudrate=9600):
        """
        Conecta na impressora via porta serial/USB virtual
        """
        try:
            self.printer = Serial(porta, baudrate=baudrate)
            self.conectada = True
            return True
        except Exception as e:
            return False, str(e)
    
    def conectar_dummy(self):
        """
        Conecta em modo dummy para testes
        """
        self.printer = Dummy()
        self.conectada = True
        return True
    
    def imprimir_comanda(self, pedido):
        """
        Imprime comanda usando comandos ESC/POS
        """
        if not self.printer:
            raise Exception("Impressora não conectada")
        
        try:
            # Cabeçalho centralizado
            self.printer.set(align='center', font='a', text_type='B', width=2, height=2)
            self.printer.text("PIZZARIA SISTEMA\n")
            
            self.printer.set(align='center', font='a', text_type='normal', width=1, height=1)
            self.printer.text("Tel: (11) 99999-9999\n")
            self.printer.text("Rua da Pizzaria, 123\n")
            self.printer.text("="*32 + "\n\n")
            
            # Informações do pedido
            self.printer.set(align='left', font='a', text_type='B')
            self.printer.text(f"COMANDA: #{limpar_texto_impressora(pedido.numero)}\n")
            
            self.printer.set(text_type='normal')
            self.printer.text(f"Data: {pedido.criado_em.strftime('%d/%m/%Y %H:%M')}\n")
            self.printer.text(f"Tipo: {limpar_texto_impressora(pedido.get_tipo_display())}\n")
            
            if pedido.cliente:
                self.printer.text(f"Cliente: {limpar_texto_impressora(pedido.cliente.nome)}\n")
                if pedido.cliente.telefone:
                    self.printer.text(f"Tel: {limpar_texto_impressora(pedido.cliente.telefone)}\n")
            
            if pedido.mesa_numero:
                self.printer.text(f"Mesa: {limpar_texto_impressora(pedido.mesa_numero)}\n")
            
            self.printer.text("-"*32 + "\n\n")
            
            # Itens
            self.printer.set(text_type='B')
            self.printer.text("ITENS DO PEDIDO:\n\n")
            self.printer.set(text_type='normal')
            
            for item in pedido.itens.all():
                nome = limpar_texto_impressora(item.produto_preco.produto.nome)
                
                # Quantidade e nome
                self.printer.text(f"{item.quantidade}x {nome}\n")
                
                # Tamanho se existir
                if item.produto_preco.tamanho:
                    self.printer.text(f"   Tam: {limpar_texto_impressora(item.produto_preco.tamanho.nome)}\n")
                
                # Observações
                if item.observacoes:
                    obs = limpar_texto_impressora(item.observacoes)
                    self.printer.text(f"   OBS: {obs}\n")
                
                # Preço alinhado à direita
                preco = f"R$ {formatar_dinheiro(item.subtotal)}"
                self.printer.set(align='right')
                self.printer.text(preco + "\n")
                self.printer.set(align='left')
                self.printer.text("\n")
            
            # Totais
            self.printer.text("-"*32 + "\n")
            
            # Subtotal
            self.printer.set(align='right')
            self.printer.text(f"Subtotal: R$ {formatar_dinheiro(pedido.subtotal)}\n")
            
            # Taxa entrega
            if pedido.taxa_entrega and pedido.taxa_entrega > 0:
                self.printer.text(f"Entrega: R$ {formatar_dinheiro(pedido.taxa_entrega)}\n")
            
            # Desconto
            if pedido.desconto and pedido.desconto > 0:
                self.printer.text(f"Desconto: -R$ {formatar_dinheiro(pedido.desconto)}\n")
            
            # Total
            self.printer.text("="*32 + "\n")
            self.printer.set(text_type='B', width=2, height=2)
            self.printer.text(f"TOTAL: R$ {formatar_dinheiro(pedido.total)}\n")
            self.printer.set(text_type='normal', width=1, height=1)
            self.printer.text("="*32 + "\n\n")
            
            # Forma de pagamento
            self.printer.set(align='left')
            if pedido.forma_pagamento:
                self.printer.text(f"Pagamento: {limpar_texto_impressora(pedido.get_forma_pagamento_display())}\n")
                
                if pedido.precisa_troco and pedido.troco_para:
                    self.printer.text(f"Troco para: R$ {formatar_dinheiro(pedido.troco_para)}\n")
            
            # Observações gerais
            if pedido.observacoes:
                self.printer.text("\nOBS: " + limpar_texto_impressora(pedido.observacoes) + "\n")
            
            # Rodapé
            self.printer.text("\n")
            self.printer.set(align='center')
            self.printer.text("-"*32 + "\n")
            self.printer.text("OBRIGADO PELA PREFERENCIA!\n")
            self.printer.text("-"*32 + "\n")
            
            # Cortar papel
            self.printer.cut()
            
            return True
            
        except Exception as e:
            raise Exception(f"Erro ao imprimir: {str(e)}")
    
    def imprimir_teste(self):
        """
        Imprime página de teste
        """
        if not self.printer:
            raise Exception("Impressora não conectada")
        
        try:
            # Teste de tamanhos - REMOVIDO printer.init()
            self.printer.set(align='center', font='a', text_type='B', width=2, height=2)
            self.printer.text("TESTE DE IMPRESSAO\n")
            
            self.printer.set(width=1, height=1)
            self.printer.text("="*32 + "\n\n")
            
            # Teste de alinhamentos
            self.printer.set(align='left')
            self.printer.text("Alinhado a esquerda\n")
            
            self.printer.set(align='center')
            self.printer.text("Centralizado\n")
            
            self.printer.set(align='right')
            self.printer.text("Alinhado a direita\n")
            
            # Teste de estilos
            self.printer.set(align='left', text_type='normal')
            self.printer.text("\nTexto normal\n")
            
            self.printer.set(text_type='B')
            self.printer.text("Texto em negrito\n")
            
            self.printer.set(text_type='U')
            self.printer.text("Texto sublinhado\n")
            
            self.printer.set(text_type='U2')
            self.printer.text("Texto sublinhado duplo\n")
            
            # Teste de código de barras
            self.printer.set(text_type='normal')
            self.printer.text("\n" + "="*32 + "\n")
            
            try:
                self.printer.barcode('123456789012', 'EAN13', 64, 2, '', '')
            except:
                self.printer.text("(Codigo de barras nao suportado)\n")
            
            # QR Code
            try:
                self.printer.qr("https://github.com/python-escpos", size=4)
            except:
                self.printer.text("(QR Code nao suportado)\n")
            
            # Finalizar
            self.printer.text("\n" + "="*32 + "\n")
            self.printer.text("IMPRESSORA FUNCIONANDO!\n")
            self.printer.text("="*32 + "\n")
            
            # Cortar
            self.printer.cut()
            
            return True
            
        except Exception as e:
            raise Exception(f"Erro no teste: {str(e)}")
    
    def desconectar(self):
        """
        Desconecta da impressora
        """
        if self.printer:
            try:
                self.printer.close()
            except:
                pass
        self.printer = None
        self.conectada = False


def detectar_impressora_windows():
    """
    Detecta impressora no Windows e retorna porta COM virtual
    """
    import subprocess
    
    try:
        # Listar portas COM
        result = subprocess.run('mode', shell=True, capture_output=True, text=True)
        
        portas_com = []
        for linha in result.stdout.split('\n'):
            if 'COM' in linha and ':' in linha:
                # Extrair número da porta COM
                import re
                match = re.search(r'COM(\d+)', linha)
                if match:
                    portas_com.append(f"COM{match.group(1)}")
        
        return portas_com
    except:
        return []


def imprimir_pedido_escpos(pedido):
    """
    Função simplificada para imprimir pedido
    """
    impressora = ImpressoraTermica()
    
    # Tentar USB primeiro
    resultado = impressora.conectar_usb()
    if not resultado:
        # Tentar portas COM
        portas = detectar_impressora_windows()
        for porta in portas:
            try:
                if impressora.conectar_serial(porta, 9600):
                    break
            except:
                continue
    
    if not impressora.conectada:
        raise Exception("Não foi possível conectar na impressora")
    
    try:
        impressora.imprimir_comanda(pedido)
        return True, "Impressão realizada com sucesso"
    except Exception as e:
        return False, str(e)
    finally:
        impressora.desconectar()