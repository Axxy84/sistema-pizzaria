# 🍕 Guia de Instalação - Sistema Pizzaria (Windows)

## 📋 Pré-requisitos

1. **Python 3.11 ou superior**
   - Baixar de: https://www.python.org/downloads/
   - ✅ Marcar "Add Python to PATH" durante instalação

2. **Node.js LTS**
   - Baixar de: https://nodejs.org/
   - Escolher versão LTS

## 🚀 Instalação Passo a Passo

### 1️⃣ Abrir PowerShell como Administrador
- Clique direito no menu Iniciar
- "Windows PowerShell (Admin)"

### 2️⃣ Navegar até a pasta
```powershell
cd C:\Users\User\Documents\sistema-pizzaria-master
```

### 3️⃣ Criar ambiente virtual Python
```powershell
python -m venv .venv
.venv\Scripts\Activate
```

### 4️⃣ Instalar dependências Python
```powershell
pip install -r requirements-windows.txt
```

Se der erro, tente:
```powershell
pip install Django==5.2.4
pip install psycopg2-binary
pip install python-dotenv
pip install supabase
pip install djangorestframework
pip install django-cors-headers
```

### 5️⃣ Configurar variáveis de ambiente
```powershell
copy .env.example .env
notepad .env
```

Editar com suas credenciais Supabase:
```
SUPABASE_URL=sua_url_aqui
SUPABASE_ANON_KEY=sua_chave_aqui
DATABASE_HOST=aws-0-sa-east-1.pooler.supabase.com
DATABASE_NAME=postgres
DATABASE_USER=postgres.aewcurtmikqelqykpqoa
DATABASE_PASSWORD=sua_senha_aqui
DATABASE_PORT=5432
USE_SUPABASE_DB=True
```

### 6️⃣ Testar o sistema
```powershell
python manage.py migrate
python manage.py runserver
```

Abrir no navegador: http://localhost:8000

## 🖥️ Criar Aplicativo Desktop (Opcional)

### 7️⃣ Entrar na pasta Electron
```powershell
cd electron
npm install
```

### 8️⃣ Criar ícone
- Converter logo.svg para icon.ico
- Site: https://convertio.co/pt/svg-ico/
- Salvar como: `electron\icon.ico`

### 9️⃣ Construir instalador
```powershell
npm run build-win
```

### 🎯 Resultado
Instalador em: `electron\dist\Sistema Pizzaria Setup 1.0.0.exe`

## 🔧 Solução de Problemas

### Erro: "python não é reconhecido"
- Reinstalar Python com "Add to PATH" marcado
- Ou usar: `py -m venv .venv`

### Erro: "cannot import psycopg2"
```powershell
pip uninstall psycopg2 psycopg2-binary
pip install psycopg2-binary
```

### Erro: "npm não é reconhecido"
- Instalar Node.js
- Reiniciar PowerShell

### Erro de conexão Supabase
- Verificar credenciais no .env
- Testar conexão internet

## 🚀 Executar o Sistema

### Opção 1: Navegador (Recomendado para teste)
```powershell
.venv\Scripts\Activate
python manage.py runserver
```
Acessar: http://localhost:8000

### Opção 2: App Desktop
Executar o instalador .exe criado

## 📞 Suporte

Em caso de dúvidas:
- Email: suporte@pizzaria.com
- WhatsApp: (11) 99999-9999

---
Versão 1.0.0 - Janeiro 2025