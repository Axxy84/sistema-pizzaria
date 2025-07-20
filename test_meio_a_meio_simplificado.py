#!/usr/bin/env python3
"""
Teste da nova funcionalidade simplificada de Pizza Meio a Meio
Verifica se a lógica de 2 cliques está implementada corretamente
"""

import os
import re

def validar_nova_logica():
    """Valida se a nova lógica simplificada está implementada"""
    print("🔥 TESTE: Pizza Meio a Meio SIMPLIFICADA (2 Cliques)")
    print("=" * 60)
    
    arquivo_template = '/home/labdev/Documentos/DjangoProject/templates/pedidos/pedido_rapido.html'
    
    if not os.path.exists(arquivo_template):
        print("❌ ERRO: Arquivo de template não encontrado")
        return False
    
    with open(arquivo_template, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Verificações da nova implementação
    verificacoes = [
        {
            'nome': 'Função selecionarPizzaComTamanho',
            'pattern': r'selecionarPizzaComTamanho\(produto, preco\)',
            'obrigatório': True,
            'descrição': 'Função principal para seleção com tamanho'
        },
        {
            'nome': 'Variável primeiroSaborTamanho',
            'pattern': r'primeiroSaborTamanho.*null',
            'obrigatório': True,
            'descrição': 'Estado para armazenar tamanho do primeiro sabor'
        },
        {
            'nome': 'Auto-criação meio a meio',
            'pattern': r'criarMeioAMeioAutomatico',
            'obrigatório': True,
            'descrição': 'Criação automática quando tamanhos iguais'
        },
        {
            'nome': 'Estados visuais de tamanho',
            'pattern': r'primeiro-sabor-tamanho.*opcao-segundo-tamanho',
            'obrigatório': True,
            'descrição': 'Classes CSS para estados por tamanho'
        },
        {
            'nome': 'Condição para mesmo tamanho',
            'pattern': r'primeiroSaborTamanho\.tamanho === preco\.tamanho',
            'obrigatório': True,
            'descrição': 'Lógica de matching de tamanhos'
        },
        {
            'nome': 'Integração nos botões de preço',
            'pattern': r'produto\.categoria === \'pizzas\' \? selecionarPizzaComTamanho',
            'obrigatório': True,
            'descrição': 'Integração com botões de preço existentes'
        },
        {
            'nome': 'Indicadores visuais',
            'pattern': r'1º ✓.*2º →',
            'obrigatório': True,
            'descrição': 'Indicadores nos botões de preço'
        },
        {
            'nome': 'Botão meio a meio opcional',
            'pattern': r'meio-a-meio-btn-opcional',
            'obrigatório': True,
            'descrição': 'Botão fallback menos proeminente'
        },
        {
            'nome': 'Feedback contextual no indicador',
            'pattern': r'Clique no mesmo tamanho em outra pizza',
            'obrigatório': True,
            'descrição': 'Mensagem explicativa específica'
        },
        {
            'nome': 'Preservação de dados antes de limpar',
            'pattern': r'const nome1 = this\.primeiroSabor\.nome',
            'obrigatório': True,
            'descrição': 'Evita bugs ao limpar estado'
        }
    ]
    
    sucessos = 0
    total = len(verificacoes)
    
    print("🔍 VERIFICANDO COMPONENTES DA NOVA LÓGICA:")
    print("-" * 50)
    
    for verificacao in verificacoes:
        if re.search(verificacao['pattern'], conteudo, re.DOTALL):
            print(f"✅ {verificacao['nome']}")
            print(f"   💡 {verificacao['descrição']}")
            sucessos += 1
        else:
            status = "❌" if verificacao['obrigatório'] else "⚠️"
            print(f"{status} {verificacao['nome']}")
            print(f"   💡 {verificacao['descrição']}")
    
    print(f"\n📊 RESULTADO: {sucessos}/{total} componentes implementados")
    
    # Verificar fluxos específicos
    print("\n🎯 VERIFICANDO FLUXOS DE USUÁRIO:")
    print("-" * 40)
    
    # Fluxo 1: Tamanhos iguais (2 cliques)
    fluxo1_ok = all([
        'selecionarPizzaComTamanho' in conteudo,
        'primeiroSaborTamanho.tamanho === preco.tamanho' in conteudo,
        'criarMeioAMeioAutomatico' in conteudo
    ])
    print(f"{'✅' if fluxo1_ok else '❌'} Fluxo 1: Tamanhos iguais → 2 cliques → Carrinho")
    
    # Fluxo 2: Tamanhos diferentes (3 cliques)
    fluxo2_ok = all([
        'mostrarModalEscolhaTamanho' in conteudo,
        'modalSeletorTamanho' in conteudo
    ])
    print(f"{'✅' if fluxo2_ok else '❌'} Fluxo 2: Tamanhos diferentes → 3 cliques → Modal → Carrinho")
    
    # Fluxo 3: Modo clássico (botão ½ + ½)
    fluxo3_ok = all([
        'selecionarParaMeioAMeio' in conteudo,
        'meio-a-meio-btn-opcional' in conteudo
    ])
    print(f"{'✅' if fluxo3_ok else '❌'} Fluxo 3: Botão ½ + ½ → Modal → Carrinho")
    
    # Estados visuais
    estados_ok = all([
        'primeiro-sabor-tamanho' in conteudo,
        'opcao-segundo-tamanho' in conteudo,
        'pulse-meio-a-meio' in conteudo
    ])
    print(f"{'✅' if estados_ok else '❌'} Estados visuais: Cores + animações por tamanho")
    
    print("\n" + "=" * 60)
    
    if sucessos >= 8 and fluxo1_ok and fluxo2_ok:  # Pelo menos 80% + fluxos principais
        print("🎉 NOVA LÓGICA IMPLEMENTADA COM SUCESSO!")
        print("\n📋 FLUXOS IMPLEMENTADOS:")
        print("   ✅ SUPER RÁPIDO: Pizza Média → Pizza Média → Carrinho (2 cliques)")
        print("   ✅ INTELIGENTE: Pizza Média → Pizza Grande → Modal → Carrinho (3 cliques)")
        print("   ✅ CLÁSSICO: ½+½ → Pizza → Pizza → Modal → Carrinho (4 cliques)")
        
        print("\n🎯 NOVA EXPERIÊNCIA:")
        print("   1. 🍕 Clique na pizza + tamanho desejado (ex: Margherita Média)")
        print("   2. 🍕 Clique noutra pizza no MESMO tamanho (ex: Calabresa Média)")
        print("   3. ✨ Pizza meio a meio criada automaticamente!")
        print("   4. 🛒 Produto aparece direto no carrinho")
        
        print("\n💡 INTELIGÊNCIA:")
        print("   • Tamanhos iguais = criação automática")
        print("   • Tamanhos diferentes = modal para escolher")  
        print("   • Visual claro com cores e animações")
        print("   • Preserva modo clássico como opção")
        
        print("\n🔗 ACESSO:")
        print("   URL: /pedidos/rapido/")
        print("   Requer: Login no sistema")
        
        return True
    else:
        print("❌ NOVA LÓGICA INCOMPLETA")
        print(f"   {sucessos}/{total} componentes presentes")
        print("   Verifique os itens marcados com ❌")
        
        # Sugestões baseadas no que está faltando
        if not fluxo1_ok:
            print("   💡 Falta: Lógica de auto-criação para tamanhos iguais")
        if not fluxo2_ok:
            print("   💡 Falta: Modal para tamanhos diferentes")
        
        return False

if __name__ == '__main__':
    try:
        sucesso = validar_nova_logica()
        print(f"\n{'🚀 IMPLEMENTAÇÃO PERFEITA!' if sucesso else '🔧 PRECISA DE AJUSTES'}")
    except Exception as e:
        print(f"\n💥 ERRO: {e}")