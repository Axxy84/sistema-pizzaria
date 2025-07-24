"""
Script para corrigir o warning do cache no settings.py
"""
import os

# Ler o arquivo settings.py
with open('DjangoProject/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir a configuração do cache
old_cache = """CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',"""

new_cache = """CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'pizzaria-cache-default',"""

content = content.replace(old_cache, new_cache)

# Fazer o mesmo para settings_fast.py
with open('settings_fast.py', 'r', encoding='utf-8') as f:
    content_fast = f.read()

content_fast = content_fast.replace(old_cache, new_cache)

# Salvar os arquivos
with open('DjangoProject/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('settings_fast.py', 'w', encoding='utf-8') as f:
    f.write(content_fast)

print("✅ Warning do cache corrigido!")