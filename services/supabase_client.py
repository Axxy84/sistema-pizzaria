from supabase import create_client, Client
from django.conf import settings
from functools import lru_cache

@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Retorna uma instância singleton do cliente Supabase.
    Usa a chave anon para operações do cliente.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
        raise ValueError("SUPABASE_URL e SUPABASE_ANON_KEY devem estar configurados no .env")
    
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

@lru_cache(maxsize=1)
def get_supabase_admin_client() -> Client:
    """
    Retorna uma instância singleton do cliente Supabase com privilégios admin.
    USE COM CUIDADO - apenas para operações administrativas do servidor.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY devem estar configurados no .env")
    
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)