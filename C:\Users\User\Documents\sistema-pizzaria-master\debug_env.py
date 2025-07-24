import os
from dotenv import load_dotenv

# Carrega .env
load_dotenv()

# Mostra as variáveis
print("=== VERIFICANDO ARQUIVO .ENV ===\n")

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')
use_supabase = os.getenv('USE_SUPABASE_DB')

print(f"SUPABASE_URL existe: {'✅' if url else '❌'}")
print(f"SUPABASE_ANON_KEY existe: {'✅' if key else '❌'}")
print(f"USE_SUPABASE_DB = {use_supabase}")

if key:
    print(f"\nTamanho da chave: {len(key)} caracteres")
    print(f"Começa com: {key[:10]}...")
    print(f"Termina com: ...{key[-10:]}")
    print(f"\nChave esperada tem 229 caracteres")
    
    # Verifica se tem quebra de linha
    if '\n' in key or '\r' in key:
        print("\n❌ ERRO: A chave tem quebra de linha!")
    else:
        print("\n✅ Chave sem quebras de linha")

print("\n=== TESTE DE CONEXÃO ===")
if url and key:
    try:
        from supabase import create_client
        client = create_client(url, key)
        response = client.table('produtos_produto').select("count").limit(1).execute()
        print("✅ CONEXÃO SUPABASE OK!")
    except Exception as e:
        print(f"❌ ERRO: {e}")
else:
    print("❌ Credenciais não encontradas no .env")