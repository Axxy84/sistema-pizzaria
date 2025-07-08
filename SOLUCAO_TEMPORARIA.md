# 🔧 Solução Temporária para Problema de Conexão IPv6

## Problema
O sistema está tentando conectar ao Supabase via IPv6, mas não há conectividade IPv6 disponível.

## Soluções Possíveis:

### 1. **Usar SQLite Localmente + Supabase API** (Recomendado por agora)
- Manter SQLite para desenvolvimento local
- Usar Supabase apenas via API REST para autenticação e dados
- Sincronizar dados importantes via API quando necessário

### 2. **Desabilitar IPv6 no Sistema**
```bash
# Temporariamente
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1

# Permanentemente (adicionar ao /etc/sysctl.conf)
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```

### 3. **Usar Conexão Pooler do Supabase**
No painel do Supabase, em Settings > Database, use a **Session pooler connection string** que geralmente funciona melhor com problemas de rede.

### 4. **Túnel SSH ou VPN**
Estabelecer um túnel que force IPv4.

## Implementação Atual

Por enquanto, vamos:
1. Voltar a usar SQLite para desenvolvimento local
2. Manter a integração com Supabase apenas para autenticação via API
3. Criar um sistema híbrido que funciona com ambos

Isso permite desenvolvimento imediato sem problemas de conectividade.