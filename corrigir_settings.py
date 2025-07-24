"""
Script para corrigir configurações do Django
"""
import os
import sys

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def corrigir_settings():
    """Corrige o arquivo settings.py adicionando middlewares faltantes"""
    
    settings_path = os.path.join(os.path.dirname(__file__), 'DjangoProject', 'settings.py')
    
    print("Verificando settings.py...")
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se AuthenticationMiddleware está presente
    if 'django.contrib.auth.middleware.AuthenticationMiddleware' not in content:
        print("❌ AuthenticationMiddleware não encontrado")
        
        # Adicionar após CsrfViewMiddleware
        content = content.replace(
            "'django.middleware.csrf.CsrfViewMiddleware',",
            "'django.middleware.csrf.CsrfViewMiddleware',\n    'django.contrib.auth.middleware.AuthenticationMiddleware',"
        )
        print("✅ AuthenticationMiddleware adicionado")
    else:
        print("✅ AuthenticationMiddleware já presente")
    
    # Verificar context_processors
    if "'django.template.context_processors.debug'" not in content:
        print("❌ context_processors incompletos")
        
        # Procurar e adicionar
        content = content.replace(
            "'context_processors': [",
            "'context_processors': [\n                'django.template.context_processors.debug',"
        )
        print("✅ context_processors corrigidos")
    
    # Salvar arquivo corrigido
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Settings.py corrigido com sucesso!")
    
    # Criar diretório static se não existir
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print("✅ Diretório 'static' criado")

if __name__ == "__main__":
    corrigir_settings()
    print("\nAgora execute novamente: instalar_windows_v2.bat")