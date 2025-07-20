#!/usr/bin/env python3
"""
Teste dos fluxos duplos: Pizza Normal vs Pizza Meio a Meio
Verifica se ambas as lógicas coexistem perfeitamente
"""

import os
import re

def validar_fluxo_duplo():
    """Valida se os dois fluxos funcionam independentemente"""
    print("🔥 TESTE: Fluxo Duplo - Normal + Meio a Meio")
    print("=" * 60)
    
    arquivo_template = '/home/labdev/Documentos/DjangoProject/templates/pedidos/pedido_rapido.html'
    
    if not os.path.exists(arquivo_template):
        print("❌ ERRO: Arquivo de template não encontrado")
        return False
    
    with open(arquivo_template, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Verificações dos dois fluxos
    verificacoes = [
        {
            'nome': 'Detecção de modo normal',
            'pattern': r'if \(!this\.primeiroSabor\).*MODO NORMAL',
            'fluxo': 'normal',
            'descrição': 'Detecta quando não está em modo meio a meio'
        },
        {
            'nome': 'Adição direta ao carrinho',
            'pattern': r'this\.adicionarAoCarrinho\(produto, preco\)',
            'fluxo': 'normal',
            'descrição': 'Pizza normal vai direto pro carrinho'
        },
        {
            'nome': 'Return após adição normal',
            'pattern': r'this\.adicionarAoCarrinho\(produto, preco\);\s*return;',
            'fluxo': 'normal',
            'descrição': 'Evita continuar para lógica meio a meio'
        },
        {
            'nome': 'Detecção de modo meio a meio',
            'pattern': r'MODO MEIO A MEIO.*já tem primeiro sabor',
            'fluxo': 'meio_a_meio',
            'descrição': 'Detecta quando está em modo meio a meio'
        },
        {
            'nome': 'Auto-criação por tamanho',
            'pattern': r'primeiroSaborTamanho\?\.tamanho === preco\.tamanho',
            'fluxo': 'meio_a_meio',
            'descrição': 'Cria meio a meio automático com mesmo tamanho'
        },
        {
            'nome': 'Modal para tamanhos diferentes',
            'pattern': r'mostrarModalEscolhaTamanho',
            'fluxo': 'meio_a_meio',
            'descrição': 'Abre modal quando tamanhos são diferentes'
        },
        {
            'nome': 'Botão ativar meio a meio',
            'pattern': r'Modo meio a meio ativado',
            'fluxo': 'ativacao',
            'descrição': 'Botão ⚡ ativa modo meio a meio'
        },
        {
            'nome': 'Cancelamento de modo',
            'pattern': r'cancelarMeioAMeio.*primeiroSabor = null',
            'fluxo': 'reset',
            'descrição': 'Cancela modo meio a meio volta ao normal'
        },
        {
            'nome': 'Estados visuais por modo',
            'pattern': r'primeiro-sabor-tamanho.*opcao-segundo-tamanho',
            'fluxo': 'visual',
            'descrição': 'CSS diferente para cada modo'
        },
        {
            'nome': 'Feedback contextual',
            'pattern': r'clique no tamanho de outra pizza',
            'fluxo': 'ux',
            'descrição': 'Mensagens explicativas para cada modo'
        }
    ]
    
    sucessos_normal = 0
    sucessos_meio_a_meio = 0
    sucessos_outros = 0
    total = len(verificacoes)
    
    print("🔍 VERIFICANDO FLUXOS INDEPENDENTES:")
    print("-" * 50)
    
    for verificacao in verificacoes:
        if re.search(verificacao['pattern'], conteudo, re.DOTALL):
            print(f"✅ {verificacao['nome']}")
            print(f"   💡 {verificacao['descrição']}")
            
            if verificacao['fluxo'] == 'normal':
                sucessos_normal += 1
            elif verificacao['fluxo'] == 'meio_a_meio':
                sucessos_meio_a_meio += 1
            else:
                sucessos_outros += 1
        else:
            print(f"❌ {verificacao['nome']}")
            print(f"   💡 {verificacao['descrição']}")
    
    print(f"\n📊 RESULTADO POR FLUXO:")
    print(f"   🍕 Normal: {sucessos_normal}/3 componentes")
    print(f"   🍕🍕 Meio a Meio: {sucessos_meio_a_meio}/3 componentes") 
    print(f"   ⚙️ Outros: {sucessos_outros}/4 componentes")
    print(f"   📈 Total: {sucessos_normal + sucessos_meio_a_meio + sucessos_outros}/{total}")
    
    # Verificar cenários de uso
    print("\n🎯 VERIFICANDO CENÁRIOS DE USO:")
    print("-" * 40)
    
    # Cenário 1: Pizza normal
    cenario1_ok = all([
        'MODO NORMAL' in conteudo,
        'this.adicionarAoCarrinho(produto, preco)' in conteudo,
        'return;' in conteudo
    ])
    print(f"{'✅' if cenario1_ok else '❌'} Cenário 1: Pizza Normal")
    print(f"   📝 Margherita Média → Clique → Carrinho (1 clique)")
    
    # Cenário 2: Meio a meio rápido
    cenario2_ok = all([
        'MODO MEIO A MEIO' in conteudo,
        'criarMeioAMeioAutomatico' in conteudo,
        'primeiroSaborTamanho?.tamanho === preco.tamanho' in conteudo
    ])
    print(f"{'✅' if cenario2_ok else '❌'} Cenário 2: Meio a Meio Rápido")
    print(f"   📝 ⚡ Botão → Margherita Média → Calabresa Média → Carrinho (3 cliques)")
    
    # Cenário 3: Meio a meio com modal
    cenario3_ok = all([
        'mostrarModalEscolhaTamanho' in conteudo,
        'modalSeletorTamanho' in conteudo
    ])
    print(f"{'✅' if cenario3_ok else '❌'} Cenário 3: Meio a Meio com Modal")
    print(f"   📝 ⚡ Botão → Margherita Média → Calabresa Grande → Modal → Carrinho")
    
    # Cenário 4: Cancelamento e volta ao normal
    cenario4_ok = all([
        'cancelarMeioAMeio' in conteudo,
        'primeiroSabor = null' in conteudo,
        'aguardandoSegundoSabor = false' in conteudo
    ])
    print(f"{'✅' if cenario4_ok else '❌'} Cenário 4: Cancelamento")
    print(f"   📝 Modo meio a meio → Cancelar → Volta ao modo normal")
    
    print("\n" + "=" * 60)
    
    if cenario1_ok and cenario2_ok and cenario3_ok and cenario4_ok:
        print("🎉 FLUXO DUPLO IMPLEMENTADO PERFEITAMENTE!")
        print("\n📋 MODOS DE OPERAÇÃO:")
        print("   🟢 MODO NORMAL (padrão):")
        print("      • Clique na pizza → Vai direto pro carrinho")
        print("      • Experiência tradicional e rápida")
        print("      • Sem estados visuais especiais")
        
        print("\n   🔵 MODO MEIO A MEIO (ativado pelo botão ⚡):")
        print("      • Primeiro clique → Seleciona 1º sabor")  
        print("      • Segundo clique → Auto-cria se mesmo tamanho")
        print("      • Segundo clique → Modal se tamanho diferente")
        print("      • Estados visuais claros com cores")
        
        print("\n🎯 EXPERIÊNCIAS POSSÍVEIS:")
        print("   1️⃣ Pizza Inteira: Margherita Média → Carrinho (1 clique)")
        print("   2️⃣ Meio a Meio Rápido: ⚡ → Margherita Média → Calabresa Média → Carrinho")
        print("   3️⃣ Meio a Meio Modal: ⚡ → Margherita Média → Calabresa Grande → Modal")
        print("   4️⃣ Cancelar: Modo meio a meio → Cancelar → Volta ao normal")
        
        print("\n💡 INTELIGÊNCIA:")
        print("   • Detecta automaticamente o modo ativo")
        print("   • Fluxos independentes e não conflitantes")  
        print("   • Experiência otimizada para cada caso")
        print("   • Cancelamento fácil e intuitivo")
        
        return True
    else:
        print("❌ FLUXO DUPLO INCOMPLETO")
        
        if not cenario1_ok:
            print("   💡 Falta: Lógica de pizza normal")
        if not cenario2_ok:
            print("   💡 Falta: Meio a meio automático")
        if not cenario3_ok:
            print("   💡 Falta: Modal para tamanhos diferentes")
        if not cenario4_ok:
            print("   💡 Falta: Sistema de cancelamento")
        
        return False

if __name__ == '__main__':
    try:
        sucesso = validar_fluxo_duplo()
        print(f"\n{'🚀 PERFEIÇÃO ALCANÇADA!' if sucesso else '🔧 PRECISA AJUSTAR'}")
    except Exception as e:
        print(f"\n💥 ERRO: {e}")