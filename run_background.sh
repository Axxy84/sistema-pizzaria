#!/bin/bash
# Script para rodar o servidor Django em segundo plano no Linux/Mac

echo "========================================"
echo "  INICIANDO SERVIDOR EM SEGUNDO PLANO"
echo "========================================"
echo

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ativa o ambiente virtual
if [ -d ".venv" ]; then
    echo "[1] Ativando ambiente virtual..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "[1] Ativando ambiente virtual..."
    source venv/bin/activate
else
    echo -e "${RED}[ERRO] Ambiente virtual não encontrado!${NC}"
    exit 1
fi

# Verifica se o Python está disponível
if ! command -v python &> /dev/null; then
    echo -e "${RED}[ERRO] Python não encontrado!${NC}"
    exit 1
fi

# Mata processos anteriores na porta 8080
echo "[2] Verificando processos na porta 8080..."
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo "   Finalizando processos existentes..."
    lsof -Pi :8080 -sTCP:LISTEN -t | xargs kill -9 2>/dev/null
fi

# Cria pasta de logs se não existir
mkdir -p logs

# Define arquivo de log com data/hora
LOGFILE="logs/server_$(date +%Y%m%d_%H%M%S).log"

echo "[3] Iniciando servidor Django em segundo plano..."
echo "    Log: $LOGFILE"
echo

# Inicia o servidor em segundo plano
nohup python run_no_auth.py > "$LOGFILE" 2>&1 &
SERVER_PID=$!

# Salva o PID
echo $SERVER_PID > server.pid

# Aguarda o servidor iniciar
sleep 3

# Verifica se o servidor está rodando
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${GREEN}[SUCESSO] Servidor rodando em segundo plano!${NC}"
    echo
    echo "URLs disponíveis:"
    echo "  - http://localhost:8080"
    echo "  - http://127.0.0.1:8080"
    echo
    echo "PID do servidor: $SERVER_PID"
    echo
    echo "Para parar o servidor: ./stop_server.sh"
    echo "Para ver os logs: tail -f $LOGFILE"
    echo
else
    echo -e "${RED}[ERRO] Servidor não iniciou corretamente!${NC}"
    echo "Verifique o log em: $LOGFILE"
    echo
    echo "Últimas linhas do log:"
    tail -n 20 "$LOGFILE"
    exit 1
fi