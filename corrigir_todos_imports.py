#!/usr/bin/env python
"""
Script para corrigir TODOS os imports de User no projeto
"""

import os
import re
from pathlib import Path

def fix_user_imports(filepath):
    """Remove import User e ajusta referências"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove import de User
        content = re.sub(r'from django\.contrib\.auth\.models import User\n?', '', content)
        
        # Substitui ForeignKey(User por ForeignKey('auth.User'
        content = re.sub(r'models\.ForeignKey\(User,', "models.ForeignKey('auth.User',", content)
        
        # Substitui outras referências diretas
        content = re.sub(r'User\.objects\.', "get_user_model().objects.", content)
        
        # Se mudou algo, salva
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Corrigido: {filepath}")
            return True
        else:
            print(f"✓ Já está OK: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Erro em {filepath}: {e}")
        return False

def main():
    """Procura e corrige todos os arquivos Python com import User"""
    
    print("="*50)
    print("CORREÇÃO DE IMPORTS DE USER")
    print("="*50)
    print()
    
    # Diretórios para buscar
    dirs_to_search = ['apps', '.', 'DjangoProject']
    
    files_fixed = 0
    files_checked = 0
    
    for dir_path in dirs_to_search:
        if os.path.exists(dir_path):
            for root, dirs, files in os.walk(dir_path):
                # Pular diretórios de ambiente virtual e cache
                if '.venv' in root or '__pycache__' in root or 'migrations' in root:
                    continue
                    
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        files_checked += 1
                        
                        # Verifica se tem o import problemático
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                if '' in f.read():
                                    if fix_user_imports(filepath):
                                        files_fixed += 1
                        except:
                            pass
    
    print()
    print("="*50)
    print(f"Arquivos verificados: {files_checked}")
    print(f"Arquivos corrigidos: {files_fixed}")
    print("="*50)
    
    if files_fixed > 0:
        print("\n⚠️  IMPORTANTE: Execute 'git pull' novamente para sincronizar!")

if __name__ == "__main__":
    main()