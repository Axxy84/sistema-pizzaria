@echo off
chcp 65001 > nul
title Correção de Imports

echo ========================================
echo   CORRIGINDO IMPORTS DOS MODELS
echo ========================================
echo.

:: Ativar ambiente virtual
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

:: Executar script Python inline para corrigir
python -c "
import os
import re

files = ['apps/pedidos/models.py', 'apps/financeiro/models.py', 'apps/estoque/models.py']

for filepath in files:
    if os.path.exists(filepath):
        print(f'Corrigindo {filepath}...')
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove linha com import User
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if 'from django.contrib.auth.models import User' not in line:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        # Substitui User por 'auth.User'
        content = re.sub(r'models\.ForeignKey\(User,', \"models.ForeignKey('auth.User',\", content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'✅ {filepath} corrigido!')
"

echo.
echo Correções aplicadas!
echo.
echo Agora execute novamente:
echo   iniciar_pizzaria.bat
echo.
pause