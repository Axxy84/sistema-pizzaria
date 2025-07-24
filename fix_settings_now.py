"""
Script direto para corrigir o settings.py
"""
import os

settings_path = 'DjangoProject/settings.py'

# Lê o arquivo
with open(settings_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Procura e corrige o MIDDLEWARE
in_middleware = False
new_lines = []
skip_next = False

for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
        
    if 'MIDDLEWARE = [' in line:
        in_middleware = True
        new_lines.append(line)
        # Adiciona o middleware correto
        new_lines.append("""    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.middleware.NoAuthMiddleware',  # Adiciona usuário falso
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
""")
        # Pula até encontrar o fim da lista
        j = i + 1
        while j < len(lines) and ']' not in lines[j]:
            j += 1
        if j < len(lines):
            new_lines.append(lines[j])  # Adiciona o ']'
        # Pula as linhas do middleware antigo
        for k in range(i + 1, j + 1):
            if k < len(lines):
                lines[k] = None
        continue
    
    if line is not None and not in_middleware:
        new_lines.append(line)
    elif line is not None and ']' in line and in_middleware:
        in_middleware = False

# Salva o arquivo corrigido
with open(settings_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Settings.py corrigido!")
print("\nMiddleware configurado corretamente:")
print("- Removido: apps.authentication.middleware_temp")
print("- Adicionado: apps.core.middleware.NoAuthMiddleware")
print("\nTente executar o servidor novamente!")