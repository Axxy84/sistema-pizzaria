#!/bin/bash
# Script para iniciar o servidor Django

echo "🍕 Iniciando Servidor Pizzaria..."
echo "==============================="

# Ativar ambiente virtual
source .venv/bin/activate

# Mostrar IP do servidor
echo "📍 Seu IP local é:"
hostname -I | awk '{print $1}'
echo "==============================="

# Coletar arquivos estáticos
echo "📦 Preparando arquivos..."
python manage.py collectstatic --noinput

# Iniciar servidor
echo "🚀 Servidor rodando!"
echo "Acesse de outros PCs: http://$(hostname -I | awk '{print $1}'):8000"
echo "==============================="

python manage.py runserver 0.0.0.0:8000