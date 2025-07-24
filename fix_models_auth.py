"""
Script para remover dependências de User dos models
"""

import os
import re

# Arquivos que precisam ser corrigidos
files_to_fix = [
    'apps/pedidos/models.py',
    'apps/financeiro/models.py',
    'apps/estoque/models.py',
]

def fix_file(filepath):
    """Remove import User e substitui referências"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove import de User
    content = re.sub(r'from django\.contrib\.auth\.models import User\n?', '', content)
    
    # Substitui ForeignKey(User por ForeignKey('auth.User'
    content = re.sub(r'models\.ForeignKey\(User,', "models.ForeignKey('auth.User',", content)
    
    # Substitui outras referências diretas a User
    content = re.sub(r'User\.objects\.', "get_user_model().objects.", content)
    
    # Adiciona import get_user_model se necessário e não existir
    if 'get_user_model' in content and 'from django.contrib.auth import get_user_model' not in content:
        # Adiciona após os imports do django.db
        content = re.sub(
            r'(from django\.db import.*\n)',
            r'\1from django.contrib.auth import get_user_model\n',
            content
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Corrigido: {filepath}")

if __name__ == "__main__":
    for file in files_to_fix:
        if os.path.exists(file):
            try:
                fix_file(file)
            except Exception as e:
                print(f"❌ Erro em {file}: {e}")
        else:
            print(f"⚠️  Arquivo não encontrado: {file}")