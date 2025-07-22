#!/bin/bash
# Script para construir o instalador Electron

echo "🍕 Construindo Sistema Pizzaria - Electron"
echo "========================================"

# Instalar dependências Node
echo "📦 Instalando dependências..."
npm install

# Copiar ícone
echo "🎨 Preparando ícones..."
cp ../static/images/logo.svg icon.svg

# Converter SVG para ICO (Windows) e PNG (Linux)
# Você precisará criar estes arquivos manualmente ou usar ferramentas online

# Garantir que Django está pronto
echo "🔧 Preparando Django..."
cd ..
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
cd electron

# Build para Windows
echo "🏗️ Construindo para Windows..."
npm run build-win

echo "✅ Build completo!"
echo "Instalador disponível em: ./dist/"
echo "========================================"