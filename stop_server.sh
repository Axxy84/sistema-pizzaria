#!/bin/bash
# Script para parar o servidor Django rodando em segundo plano

echo "========================================"
echo "  PARANDO SERVIDOR DJANGO"
echo "========================================"
echo

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se existe arquivo com PID
if [ -f server.pid ]; then
    PID=$(cat server.pid)
    echo "[1] Parando processo com PID: $PID"
    kill -9 $PID 2>/dev/null
    rm server.pid
else
    echo -e "${YELLOW}[1] Arquivo server.pid não encontrado${NC}"
fi

# Para garantir, mata todos os processos na porta 8080
echo "[2] Verificando outros processos na porta 8080..."
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo "   Finalizando processos encontrados..."
    lsof -Pi :8080 -sTCP:LISTEN -t | xargs kill -9 2>/dev/null
fi

# Verifica se ainda há processos
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo
    echo -e "${RED}[AVISO] Ainda existem processos na porta 8080${NC}"
    echo "Tente executar com sudo: sudo ./stop_server.sh"
else
    echo
    echo -e "${GREEN}[SUCESSO] Servidor parado com sucesso!${NC}"
fi

echo