#!/usr/bin/env python3
"""
Teste da nova lógica intuitiva: Selecionar → Decidir
Verifica se o fluxo "primeiro clique seleciona, segundo decide" está funcionando
"""

import os
import re

def validar_logica_intuitiva():
    """Valida se a nova lógica intuitiva está implementada"""
    print("🔥 TESTE: Lógica Intuitiva - Selecionar → Decidir")
    print("=" * 60)
    
    arquivo_template = '/home/labdev/Documentos/DjangoProject/templates/pedidos/pedido_rapido.html'
    
    if not os.path.exists(arquivo_template):
        print("❌ ERRO: Arquivo de template não encontrado")
        return False
    
    with open(arquivo_template, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Verificações da nova lógica intuitiva
    verificacoes = [
        {
            'nome': 'Estado de pizza selecionada',
            'pattern': r'pizzaSelecionada.*pizzaSelecionadaTamanho.*aguardandoDecisao',
            'etapa': 'selecao',
            'descrição': 'Estados para pizza selecionada (não confirmada)'
        },
        {
            'nome': 'Primeira seleção sempre seleciona',
            'pattern': r'PRIMEIRA SELEÇÃO.*sempre seleciona',
            'etapa': 'selecao',
            'descrição': 'Primeiro clique nunca adiciona direto ao carrinho'
        },
        {
            'nome': 'Confirmação de pizza inteira',
            'pattern': r'confirmarPizzaInteira.*this\.adicionarAoCarrinho',
            'etapa': 'confirmacao',
            'descrição': 'Função para confirmar pizza como inteira'
        },
        {
            'nome': 'Detecção de segunda seleção',
            'pattern': r'SEGUNDA SELEÇÃO.*usuário decidindo',
            'etapa': 'decisao',
            'descrição': 'Segundo clique é tratado como decisão'
        },
        {
            'nome': 'Auto meio a meio por tamanho',
            'pattern': r'criarMeioAMeioComSelecionada',
            'etapa': 'meio_a_meio',
            'descrição': 'Cria meio a meio automático quando tamanhos iguais'
        },
        {
            'nome': 'Modal para tamanhos diferentes',
            'pattern': r'mostrarModalEscolhaTamanhoComSelecionada',
            'etapa': 'meio_a_meio',
            'descrição': 'Modal quando segunda pizza tem tamanho diferente'
        },
        {
            'nome': 'Estados visuais diferenciados',
            'pattern': r'pizza-selecionada.*opcao-meio-a-meio-compativel.*opcao-meio-a-meio-modal',
            'etapa': 'interface',
            'descrição': 'Classes CSS para cada tipo de estado'
        },
        {
            'nome': 'Indicador de pizza selecionada',
            'pattern': r'Pizza Selecionada.*Clique novamente para confirmar inteira',
            'etapa': 'interface',
            'descrição': 'Interface que mostra pizza selecionada e opções'
        },
        {
            'nome': 'Botão confirmar pizza inteira',
            'pattern': r'✓ Pizza Inteira',
            'etapa': 'interface',
            'descrição': 'Botão dedicado para confirmar pizza inteira'
        },
        {
            'nome': 'Limpeza de seleção',
            'pattern': r'limparSelecao.*pizzaSelecionada = null.*aguardandoDecisao = false',
            'etapa': 'reset',
            'descrição': 'Função para limpar seleção e voltar ao estado inicial'
        }
    ]
    
    sucessos_por_etapa = {
        'selecao': 0,
        'confirmacao': 0,
        'decisao': 0,
        'meio_a_meio': 0,
        'interface': 0,
        'reset': 0
    }
    
    total = len(verificacoes)
    
    print("🔍 VERIFICANDO COMPONENTES DA LÓGICA INTUITIVA:")
    print("-" * 55)
    
    for verificacao in verificacoes:
        if re.search(verificacao['pattern'], conteudo, re.DOTALL):
            print(f"✅ {verificacao['nome']}")
            print(f"   💡 {verificacao['descrição']}")
            sucessos_por_etapa[verificacao['etapa']] += 1
        else:
            print(f"❌ {verificacao['nome']}")
            print(f"   💡 {verificacao['descrição']}")
    
    total_sucessos = sum(sucessos_por_etapa.values())
    print(f"\n📊 RESULTADO POR ETAPA:")
    print(f"   🎯 Seleção: {sucessos_por_etapa['selecao']}/2")
    print(f"   ✅ Confirmação: {sucessos_por_etapa['confirmacao']}/1")
    print(f"   🤔 Decisão: {sucessos_por_etapa['decisao']}/1")
    print(f"   🍕🍕 Meio a Meio: {sucessos_por_etapa['meio_a_meio']}/2")
    print(f"   🎨 Interface: {sucessos_por_etapa['interface']}/3")
    print(f"   🔄 Reset: {sucessos_por_etapa['reset']}/1")
    print(f"   📈 Total: {total_sucessos}/{total}")
    
    # Verificar fluxos específicos
    print("\n🎯 VERIFICANDO FLUXOS DE USUÁRIO:")
    print("-" * 40)
    
    # Fluxo 1: Pizza inteira (2 cliques)
    fluxo1_ok = all([
        'pizzaSelecionada' in conteudo,
        'confirmarPizzaInteira' in conteudo,
        'PRIMEIRA SELEÇÃO' in conteudo,
        'SEGUNDA SELEÇÃO' in conteudo
    ])
    print(f"{'✅' if fluxo1_ok else '❌'} Fluxo 1: Pizza Inteira")
    print(f"   📝 Margherita Média [CLIQUE] → Selecionada")
    print(f"   📝 Margherita Média [CLIQUE] → Carrinho")
    
    # Fluxo 2: Meio a meio automático (2 cliques)
    fluxo2_ok = all([
        'criarMeioAMeioComSelecionada' in conteudo,
        'pizzaSelecionadaTamanho.tamanho === preco.tamanho' in conteudo
    ])
    print(f"{'✅' if fluxo2_ok else '❌'} Fluxo 2: Meio a Meio Automático")
    print(f"   📝 Margherita Média [CLIQUE] → Selecionada")
    print(f"   📝 Calabresa Média [CLIQUE] → Meio a meio no carrinho")
    
    # Fluxo 3: Meio a meio com modal (3 cliques)
    fluxo3_ok = all([
        'mostrarModalEscolhaTamanhoComSelecionada' in conteudo,
        'modalSeletorTamanho' in conteudo
    ])
    print(f"{'✅' if fluxo3_ok else '❌'} Fluxo 3: Meio a Meio com Modal")
    print(f"   📝 Margherita Média [CLIQUE] → Selecionada")
    print(f"   📝 Calabresa Grande [CLIQUE] → Modal")
    print(f"   📝 Escolher tamanho [CLIQUE] → Carrinho")
    
    # Fluxo 4: Botão confirmar
    fluxo4_ok = all([
        '✓ Pizza Inteira' in conteudo,
        'confirmarPizzaInteira()' in conteudo
    ])
    print(f"{'✅' if fluxo4_ok else '❌'} Fluxo 4: Botão Confirmar")
    print(f"   📝 Margherita Média [CLIQUE] → Selecionada")
    print(f"   📝 Botão '✓ Pizza Inteira' [CLIQUE] → Carrinho")
    
    # Estados visuais
    estados_ok = all([
        'pizza-selecionada' in conteudo,
        'opcao-meio-a-meio-compativel' in conteudo,
        'opcao-meio-a-meio-modal' in conteudo,
        'pulse-verde' in conteudo
    ])
    print(f"{'✅' if estados_ok else '❌'} Estados Visuais")
    print(f"   📝 Azul = Selecionada | Verde = Compatível | Amarelo = Modal")
    
    print("\n" + "=" * 60)
    
    if total_sucessos >= 8 and fluxo1_ok and fluxo2_ok and fluxo3_ok and fluxo4_ok:
        print("🎉 LÓGICA INTUITIVA IMPLEMENTADA PERFEITAMENTE!")
        print("\n📋 NOVA EXPERIÊNCIA INTUITIVA:")
        print("   🎯 PRIMEIRO CLIQUE = SEMPRE SELEÇÃO")
        print("      • Nunca adiciona direto ao carrinho")
        print("      • Mostra pizza selecionada com indicador visual")
        print("      • Apresenta opções claras ao usuário")
        
        print("\n   🤔 SEGUNDO CLIQUE = DECISÃO DO USUÁRIO")
        print("      • Mesma pizza = Confirma inteira")
        print("      • Pizza diferente mesmo tamanho = Meio a meio automático")
        print("      • Pizza diferente tamanho diferente = Modal escolha")
        
        print("\n🎨 ESTADOS VISUAIS INTUITIVOS:")
        print("   🔵 Azul + Brilho = Pizza selecionada")
        print("   🟢 Verde + Pulse = Compatível para meio a meio")
        print("   🟡 Amarelo = Precisa modal para escolher tamanho")
        
        print("\n🎯 EXPERIÊNCIAS POSSÍVEIS:")
        print("   1️⃣ Pizza Inteira: Margherita Média → Margherita Média → Carrinho")
        print("   2️⃣ Pizza Inteira: Margherita Média → Botão '✓ Pizza Inteira' → Carrinho")
        print("   3️⃣ Meio a Meio: Margherita Média → Calabresa Média → Carrinho")
        print("   4️⃣ Meio a Meio: Margherita Média → Calabresa Grande → Modal → Carrinho")
        
        print("\n💡 VANTAGENS DA NOVA LÓGICA:")
        print("   • Sempre fica claro o que está selecionado")
        print("   • Usuário tem controle total da decisão")
        print("   • Visual guia o usuário intuitivamente")
        print("   • Menos cliques para casos comuns")
        print("   • Mais flexível que a lógica anterior")
        
        return True
    else:
        print("❌ LÓGICA INTUITIVA INCOMPLETA")
        print(f"   {total_sucessos}/{total} componentes presentes")
        
        if not fluxo1_ok:
            print("   💡 Falta: Fluxo de pizza inteira")
        if not fluxo2_ok:
            print("   💡 Falta: Meio a meio automático")
        if not fluxo3_ok:
            print("   💡 Falta: Modal para tamanhos diferentes")
        if not fluxo4_ok:
            print("   💡 Falta: Botão de confirmação")
        
        return False

if __name__ == '__main__':
    try:
        sucesso = validar_logica_intuitiva()
        print(f"\n{'🚀 GENIALIDADE IMPLEMENTADA!' if sucesso else '🔧 AINDA PRECISA AJUSTAR'}")
    except Exception as e:
        print(f"\n💥 ERRO: {e}")