"""
Utilitários para impressão em impressoras térmicas
Corrige problemas de codificação de caracteres
"""

import unicodedata
import re
from decimal import Decimal
from datetime import datetime
import os
import subprocess

def limpar_texto_impressora(texto):
    """
    Remove acentos e caracteres especiais que causam problemas na impressora térmica
    """
    if not texto:
        return ""
    
    # Converter para string se necessário
    texto = str(texto)
    
    # Remover acentos usando unicodedata
    texto_sem_acentos = unicodedata.normalize('NFKD', texto)
    texto_sem_acentos = ''.join([c for c in texto_sem_acentos if not unicodedata.combining(c)])
    
    # Substituições específicas para português
    substituicoes = {
        'ç': 'c', 'Ç': 'C',
        'ã': 'a', 'Ã': 'A',
        'õ': 'o', 'Õ': 'O',
        'ñ': 'n', 'Ñ': 'N',
        '°': 'o',
        '–': '-', '—': '-',
        ''': "'", ''': "'",
        '"': '"', '"': '"',
    }
    
    for original, substituto in substituicoes.items():
        texto_sem_acentos = texto_sem_acentos.replace(original, substituto)
    
    # Manter apenas caracteres ASCII imprimíveis
    texto_limpo = ''.join(char if ord(char) < 128 and char.isprintable() or char in '\n\r\t ' else '?' for char in texto_sem_acentos)
    
    return texto_limpo

def formatar_dinheiro(valor):
    """
    Formata valor monetário sem símbolo especial
    """
    if not valor:
        return "0,00"
    
    try:
        valor_decimal = Decimal(str(valor))
        return f"{valor_decimal:.2f}".replace('.', ',')
    except:
        return "0,00"

def gerar_comanda_texto_puro(pedido):
    """
    Gera comanda em texto puro para impressora térmica
    """
    linhas = []
    
    # Cabeçalho
    linhas.append("=" * 40)
    linhas.append("         PIZZARIA SISTEMA")
    linhas.append("     Tel: (11) 99999-9999")
    linhas.append("  Rua da Pizzaria, 123 - Centro")
    linhas.append("=" * 40)
    linhas.append("")
    
    # Informações do pedido
    linhas.append(f"COMANDA: #{limpar_texto_impressora(pedido.numero)}")
    linhas.append(f"Data: {pedido.criado_em.strftime('%d/%m/%Y %H:%M')}")
    linhas.append(f"Tipo: {limpar_texto_impressora(pedido.get_tipo_display())}")
    
    if pedido.cliente:
        linhas.append(f"Cliente: {limpar_texto_impressora(pedido.cliente.nome)}")
        if pedido.cliente.telefone:
            linhas.append(f"Telefone: {limpar_texto_impressora(pedido.cliente.telefone)}")
    
    if pedido.mesa_numero:
        linhas.append(f"Mesa: {limpar_texto_impressora(pedido.mesa_numero)}")
    
    if pedido.endereco_entrega:
        endereco_limpo = limpar_texto_impressora(str(pedido.endereco_entrega))
        if len(endereco_limpo) > 35:
            endereco_limpo = endereco_limpo[:32] + "..."
        linhas.append(f"Endereco: {endereco_limpo}")
    
    linhas.append("-" * 40)
    linhas.append("")
    
    # Itens do pedido
    linhas.append("ITENS DO PEDIDO:")
    linhas.append("")
    
    for item in pedido.itens.all():
        nome_produto = limpar_texto_impressora(item.produto_preco.produto.nome)
        if len(nome_produto) > 25:
            nome_produto = nome_produto[:22] + "..."
        
        # Linha principal do item
        linha_item = f"{item.quantidade}x {nome_produto}"
        preco_item = f"R$ {formatar_dinheiro(item.subtotal)}"
        
        # Ajustar espaçamento
        espacos_necessarios = 40 - len(linha_item) - len(preco_item)
        if espacos_necessarios > 0:
            linha_item += " " * espacos_necessarios + preco_item
        else:
            linha_item += " " + preco_item
        
        linhas.append(linha_item)
        
        # Tamanho se existir
        if item.produto_preco.tamanho:
            tamanho_texto = limpar_texto_impressora(item.produto_preco.tamanho.nome)
            linhas.append(f"  Tamanho: {tamanho_texto}")
        
        # Observações se existir
        if item.observacoes:
            obs_limpa = limpar_texto_impressora(item.observacoes)
            if len(obs_limpa) > 35:
                # Quebrar em múltiplas linhas
                palavras = obs_limpa.split()
                linha_atual = "  OBS: "
                for palavra in palavras:
                    if len(linha_atual + palavra) <= 38:
                        linha_atual += palavra + " "
                    else:
                        linhas.append(linha_atual.rstrip())
                        linha_atual = "       " + palavra + " "
                if linha_atual.strip():
                    linhas.append(linha_atual.rstrip())
            else:
                linhas.append(f"  OBS: {obs_limpa}")
        
        # Para pizza meio a meio
        if hasattr(item, 'is_meio_a_meio') and item.is_meio_a_meio:
            sabor1 = limpar_texto_impressora(str(item.sabor_1))
            sabor2 = limpar_texto_impressora(str(item.sabor_2))
            linhas.append(f"  MEIO A MEIO: {sabor1} + {sabor2}")
        
        linhas.append("")
    
    # Totais
    linhas.append("-" * 40)
    
    subtotal_str = f"Subtotal: R$ {formatar_dinheiro(pedido.subtotal)}"
    espacos = 40 - len(subtotal_str)
    linhas.append(" " * espacos + subtotal_str)
    
    if pedido.taxa_entrega and pedido.taxa_entrega > 0:
        taxa_str = f"Taxa Entrega: R$ {formatar_dinheiro(pedido.taxa_entrega)}"
        espacos = 40 - len(taxa_str)
        linhas.append(" " * espacos + taxa_str)
    
    if pedido.desconto and pedido.desconto > 0:
        desconto_str = f"Desconto: -R$ {formatar_dinheiro(pedido.desconto)}"
        espacos = 40 - len(desconto_str)
        linhas.append(" " * espacos + desconto_str)
    
    linhas.append("=" * 40)
    total_str = f"TOTAL: R$ {formatar_dinheiro(pedido.total)}"
    espacos = 40 - len(total_str)
    linhas.append(" " * espacos + total_str)
    linhas.append("=" * 40)
    linhas.append("")
    
    # Forma de pagamento
    if pedido.forma_pagamento:
        pagamento_display = limpar_texto_impressora(pedido.get_forma_pagamento_display())
        linhas.append(f"Pagamento: {pagamento_display}")
        
        if pedido.precisa_troco and pedido.troco_para:
            linhas.append(f"Troco para: R$ {formatar_dinheiro(pedido.troco_para)}")
        
        linhas.append("")
    
    # Observações gerais
    if pedido.observacoes:
        linhas.append("OBSERVACOES:")
        obs_geral = limpar_texto_impressora(pedido.observacoes)
        
        # Quebrar observações em linhas de até 40 caracteres
        palavras = obs_geral.split()
        linha_atual = ""
        for palavra in palavras:
            if len(linha_atual + palavra) <= 38:
                linha_atual += palavra + " "
            else:
                if linha_atual.strip():
                    linhas.append(linha_atual.rstrip())
                linha_atual = palavra + " "
        if linha_atual.strip():
            linhas.append(linha_atual.rstrip())
        
        linhas.append("")
    
    # Rodapé
    linhas.append("-" * 40)
    linhas.append("     OBRIGADO PELA PREFERENCIA!")
    linhas.append(f"     {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    linhas.append("")
    linhas.append("")
    linhas.append("")  # Espaço para corte do papel
    
    return "\n".join(linhas)

def salvar_comanda_arquivo(pedido, caminho=None):
    """
    Salva comanda em arquivo de texto para impressão
    """
    if not caminho:
        caminho = f"comanda_{pedido.numero}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    comanda_texto = gerar_comanda_texto_puro(pedido)
    
    # Salvar com codificação compatível com impressora térmica
    try:
        # Primeiro tentar com cp850 (padrão para impressoras térmicas)
        with open(caminho, 'w', encoding='cp850', errors='replace') as f:
            f.write(comanda_texto)
    except:
        try:
            # Fallback para latin-1
            with open(caminho, 'w', encoding='latin-1', errors='replace') as f:
                f.write(comanda_texto)
        except:
            # Último recurso: ASCII puro
            with open(caminho, 'w', encoding='ascii', errors='replace') as f:
                f.write(comanda_texto)
    
    return caminho

def obter_porta_knup():
    """
    Obtém a porta USB configurada para a impressora KNUP
    """
    # Primeiro, verificar se existe arquivo de configuração
    if os.path.exists('knup_porta.txt'):
        try:
            with open('knup_porta.txt', 'r') as f:
                porta = f.read().strip()
                if porta:
                    return porta
        except:
            pass
    
    # Se não, tentar detectar automaticamente
    for porta in ['USB001', 'USB002', 'USB003']:
        # Testar se a porta existe tentando copiar um arquivo vazio
        try:
            with open('test_porta.tmp', 'w') as f:
                f.write('')
            
            result = subprocess.run(f'copy test_porta.tmp {porta}', 
                                  shell=True, capture_output=True, timeout=2)
            
            os.unlink('test_porta.tmp')
            
            if result.returncode == 0:
                # Salvar para próxima vez
                with open('knup_porta.txt', 'w') as f:
                    f.write(porta)
                return porta
        except:
            pass
    
    return None

def imprimir_comanda_windows(pedido, impressora=None):
    """
    Imprime comanda no Windows via comando copy direto para USB
    """
    import tempfile
    
    # Gerar arquivo temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='cp850', errors='replace') as f:
        comanda_texto = gerar_comanda_texto_puro(pedido)
        f.write(comanda_texto)
        arquivo_temp = f.name
    
    try:
        # Obter porta USB da KNUP
        porta_usb = obter_porta_knup()
        
        if porta_usb:
            # Usar COPY direto para a porta USB
            cmd = f'copy "{arquivo_temp}" {porta_usb}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, f"Impressão enviada com sucesso para {porta_usb}"
            else:
                return False, f"Erro ao enviar para {porta_usb}: {result.stderr}"
        else:
            # Fallback: tentar comando print
            if impressora:
                cmd = f'print /D:"{impressora}" "{arquivo_temp}"'
            else:
                cmd = f'print "{arquivo_temp}"'
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "Impressão enviada com sucesso"
            else:
                return False, f"Erro na impressão: {result.stderr}"
    
    except Exception as e:
        return False, f"Erro ao imprimir: {str(e)}"
    
    finally:
        # Limpar arquivo temporário
        try:
            os.unlink(arquivo_temp)
        except:
            pass