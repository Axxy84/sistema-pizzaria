#!/usr/bin/env python
import os
import sys
import re

def find_status_references(directory):
    """Busca por referências ao campo status nos arquivos Python"""
    patterns = [
        r'\.filter\([^)]*status[^)]*\)',
        r'\.exclude\([^)]*status[^)]*\)',
        r'pedido\.status\s*=',
        r'get_status_display',
        r'STATUS_CHOICES'
    ]
    
    for root, dirs, files in os.walk(directory):
        # Ignorar diretórios
        if any(d in root for d in ['.venv', '__pycache__', 'migrations', '.git']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for i, line in enumerate(content.split('\n'), 1):
                        for pattern in patterns:
                            if re.search(pattern, line):
                                print(f"{filepath}:{i}: {line.strip()}")
                except Exception as e:
                    pass

if __name__ == "__main__":
    print("=== Buscando referências ao campo status antigo ===\n")
    find_status_references('apps/pedidos/')
    print("\n=== Busca concluída ===")