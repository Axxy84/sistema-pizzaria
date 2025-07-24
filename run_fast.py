#!/usr/bin/env python
"""
Script para rodar Django com configurações otimizadas
Sem autenticação, focado em performance
"""

import os
import sys

if __name__ == "__main__":
    # Usar configurações otimizadas
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_fast")
    
    # Desabilitar checagens desnecessárias
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Executar com otimizações
    sys.argv = [sys.argv[0], 'runserver', '0.0.0.0:8000', '--noreload', '--nothreading']
    
    print("\n" + "="*60)
    print("🚀 SERVIDOR OTIMIZADO PARA PERFORMANCE")
    print("="*60)
    print("✅ Sem autenticação")
    print("✅ Cache em memória")
    print("✅ Queries otimizadas")
    print("✅ Middleware mínimo")
    print("✅ Templates cacheados")
    print("\n📍 Acesse: http://localhost:8000")
    print("="*60 + "\n")
    
    execute_from_command_line(sys.argv)