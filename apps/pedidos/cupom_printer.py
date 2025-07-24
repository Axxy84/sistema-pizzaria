import unicodedata
from datetime import datetime

def remover_acentos(texto):
    """Remove acentos do texto para compatibilidade com impressora térmica"""
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

def gerar_cupom_texto(pedido):
    """Gera cupom em texto puro para impressora térmica"""
    linhas = []
    
    # Cabeçalho
    linhas.append("="*40)
    linhas.append("         PIZZARIA SISTEMA")
    linhas.append("="*40)
    linhas.append("")
    
    # Dados do pedido
    linhas.append(f"COMANDA: {pedido.get('numero', '000000')}")
    linhas.append(f"Cliente: {remover_acentos(pedido.get('cliente', 'Balcao'))}")
    linhas.append(f"Tipo: {remover_acentos(pedido.get('tipo', 'Balcao'))}")
    linhas.append(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    linhas.append("-"*40)
    
    # Itens
    linhas.append("ITENS:")
    linhas.append("")
    
    total = 0
    for item in pedido.get('itens', []):
        nome = remover_acentos(item.get('nome', ''))
        qtd = item.get('quantidade', 1)
        valor = item.get('valor', 0)
        total += valor * qtd
        
        linhas.append(f"- {nome}")
        if item.get('descricao'):
            desc = remover_acentos(item.get('descricao', ''))
            linhas.append(f"  {desc}")
        linhas.append(f"  Qtd: {qtd}  Valor: R$ {valor:.2f}")
        linhas.append("")
    
    # Total
    linhas.append("-"*40)
    linhas.append(f"TOTAL: R$ {total:.2f}")
    linhas.append("-"*40)
    
    # Observações
    if pedido.get('observacoes'):
        linhas.append("OBS: " + remover_acentos(pedido.get('observacoes', '')))
        linhas.append("")
    
    # Rodapé
    linhas.append("")
    linhas.append("     OBRIGADO PELA PREFERENCIA!")
    linhas.append("")
    linhas.append("")
    linhas.append("")  # Espaço para corte
    
    return "\n".join(linhas)

def salvar_cupom_arquivo(pedido, caminho="cupom_temp.txt"):
    """Salva cupom em arquivo texto"""
    cupom_texto = gerar_cupom_texto(pedido)
    
    # Salvar em codificação compatível com impressora
    with open(caminho, 'w', encoding='cp850') as f:
        f.write(cupom_texto)
    
    return caminho

def imprimir_cupom_windows(pedido, nome_impressora=None):
    """Imprime cupom usando comandos Windows"""
    import subprocess
    
    # Gerar arquivo
    arquivo = salvar_cupom_arquivo(pedido)
    
    # Comando de impressão
    if nome_impressora:
        cmd = f'print /D:"{nome_impressora}" {arquivo}'
    else:
        cmd = f'notepad /p {arquivo}'
    
    # Executar
    subprocess.run(cmd, shell=True)
    
    return True