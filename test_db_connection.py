import os
import socket
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Força resolução IPv4
original_getaddrinfo = socket.getaddrinfo

def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
    return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

socket.getaddrinfo = getaddrinfo_ipv4_only

# Tenta conexão direta
try:
    conn = psycopg2.connect(
        host=os.getenv('DATABASE_HOST'),
        database=os.getenv('DATABASE_NAME'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        port=os.getenv('DATABASE_PORT'),
        sslmode='require'
    )
    print("✅ Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
    
# Mostra as variáveis
print("\n📋 Configurações:")
print(f"HOST: {os.getenv('DATABASE_HOST')}")
print(f"DATABASE: {os.getenv('DATABASE_NAME')}")
print(f"USER: {os.getenv('DATABASE_USER')}")
print(f"PASSWORD: {'*' * len(os.getenv('DATABASE_PASSWORD', ''))}")
print(f"PORT: {os.getenv('DATABASE_PORT')}")