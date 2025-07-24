#!/usr/bin/env python
"""
Script para remover todas as referências a login dos templates
"""
import os
import re

def remover_login_templates():
    """Remove referências a login dos templates"""
    
    # Templates para corrigir
    templates = [
        'templates/authentication/register.html',
        'templates/authentication/django_login.html',
        'templates/base.html',
        'templates/base/navbar.html'
    ]
    
    for template_path in templates:
        if os.path.exists(template_path):
            print(f"Processando {template_path}...")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Substituir {% url 'login' %} por /
            content = re.sub(r"\{%\s*url\s+['\"]login['\"]\s*%\}", "/", content)
            
            # Remover links de login do navbar
            content = re.sub(
                r'<a[^>]*href="[^"]*login[^"]*"[^>]*>.*?</a>',
                '<!-- Login removido - sistema sem autenticação -->',
                content,
                flags=re.DOTALL
            )
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {template_path} corrigido")
        else:
            print(f"⚠️ {template_path} não encontrado")

def criar_urls_dummy():
    """Cria URLs dummy para evitar erros"""
    
    urls_auth = '''from django.urls import path
from django.shortcuts import redirect

app_name = 'authentication'

# URLs dummy - sistema sem autenticação
def dummy_view(request):
    return redirect('home')

urlpatterns = [
    path('login/', dummy_view, name='login'),
    path('logout/', dummy_view, name='logout'),
    path('register/', dummy_view, name='register'),
]
'''
    
    # Criar arquivo de URLs
    os.makedirs('apps/authentication', exist_ok=True)
    
    # Criar __init__.py
    open('apps/authentication/__init__.py', 'a').close()
    
    with open('apps/authentication/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_auth)
    
    print("✅ URLs dummy criadas em apps/authentication/urls.py")

if __name__ == "__main__":
    print("=== REMOVENDO REFERÊNCIAS A LOGIN ===\n")
    
    # 1. Corrigir templates
    remover_login_templates()
    
    print("\n")
    
    # 2. Criar URLs dummy
    criar_urls_dummy()
    
    print("\n✅ CORREÇÃO CONCLUÍDA!")
    print("\nAgora você precisa adicionar no urls.py principal:")
    print("path('auth/', include('apps.authentication.urls')),")