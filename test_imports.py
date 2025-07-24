#!/usr/bin/env python
"""
Teste básico de importações e configurações do Django
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

def test_imports():
    """Testa se os modelos podem ser importados sem erros"""
    print("=== TESTE DE IMPORTAÇÕES ===\n")
    
    tests = []
    
    # Teste 1: Importar User
    try:
        from django.contrib.auth.models import User
        tests.append(("Import User", "✅ OK"))
    except Exception as e:
        tests.append(("Import User", f"❌ ERRO: {e}"))
    
    # Teste 2: Importar modelos financeiro
    try:
        from apps.financeiro.models import Caixa, MovimentoCaixa, ContaPagar
        tests.append(("Import Financeiro Models", "✅ OK"))
    except Exception as e:
        tests.append(("Import Financeiro Models", f"❌ ERRO: {e}"))
    
    # Teste 3: Importar modelos settings
    try:
        from settings.models import UserPreference
        tests.append(("Import Settings Models", "✅ OK"))
    except Exception as e:
        tests.append(("Import Settings Models", f"❌ ERRO: {e}"))
    
    # Teste 4: Testar views
    try:
        from DjangoProject.views import home_view, dashboard_data_api
        tests.append(("Import Views", "✅ OK"))
    except Exception as e:
        tests.append(("Import Views", f"❌ ERRO: {e}"))
    
    # Teste 5: Verificar apps instalados
    try:
        from django.conf import settings
        app_count = len(settings.INSTALLED_APPS)
        tests.append(("Apps Instalados", f"✅ {app_count} apps"))
    except Exception as e:
        tests.append(("Apps Instalados", f"❌ ERRO: {e}"))
    
    # Exibir resultados
    for test_name, result in tests:
        print(f"{test_name}: {result}")
    
    # Resumo
    passed = sum(1 for _, r in tests if "✅" in r)
    total = len(tests)
    print(f"\n=== RESUMO: {passed}/{total} testes passaram ===")
    
    return passed == total

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)