import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega .env
load_dotenv()

# Pega as variáveis
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')

print(f"URL: {url}")
print(f"KEY: {key[:20]}...{key[-20:] if key else 'NONE'}")

try:
    # Tenta conectar
    supabase: Client = create_client(url, key)
    
    # Testa uma query simples
    response = supabase.table('produtos_produto').select("*").limit(1).execute()
    print("\n✅ Conexão OK!")
    print(f"Resposta: {response}")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    print("\nVerifique:")
    print("1. A chave está completa em uma linha")
    print("2. Não tem espaços extras")
    print("3. As credenciais estão corretas no Supabase")