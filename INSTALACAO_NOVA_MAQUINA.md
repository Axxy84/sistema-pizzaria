# 🖥️ Instalação em Nova Máquina - Sistema de Pizzaria

## 📋 Pré-requisitos

### Software Necessário
```bash
# 1. Python 3.13 (ou 3.11+)
python --version  # Verificar se está instalado

# 2. Git
git --version

# 3. pip (geralmente vem com Python)
pip --version
```

---

## 📁 Passo 1: Clonar/Copiar o Projeto

### Opção A: Se o projeto está no Git
```bash
git clone <url-do-repositorio>
cd DjangoProject
```

### Opção B: Copiar arquivos manualmente
```bash
# Copiar toda a pasta DjangoProject para a nova máquina
# Pode usar pendrive, compartilhamento de rede, etc.
```

---

## 🐍 Passo 2: Criar Ambiente Virtual

```bash
# Navegar para o diretório do projeto
cd DjangoProject

# Criar ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual
# No Windows:
.venv\Scripts\activate

# No Linux/Mac:
source .venv/bin/activate

# Verificar se está ativo (deve aparecer (.venv) no prompt)
```

---

## 📦 Passo 3: Instalar Dependências

```bash
# Com o ambiente virtual ativo, instalar dependências
pip install -r requirements.txt

# Se der erro, tentar atualizar pip primeiro:
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Passo 4: Configurar Variáveis de Ambiente

```bash
# Copiar o template de configuração
cp .env.example .env

# Editar o arquivo .env com suas configurações
# No Windows: notepad .env
# No Linux: nano .env ou gedit .env
```

### Configurações mínimas no .env:
```bash
# Para desenvolvimento local (SQLite)
SECRET_KEY=django-insecure-sua-chave-aqui
DEBUG=True
USE_SUPABASE_DB=False

# OU para produção (Supabase)
SECRET_KEY=sua-chave-secreta-super-segura
DEBUG=False
USE_SUPABASE_DB=True
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua_anon_key
SUPABASE_SERVICE_ROLE_KEY=sua_service_key
DATABASE_USER=postgres.sua_ref_projeto
DATABASE_PASSWORD=sua_senha_banco
```

---

## 🗄️ Passo 5: Configurar Banco de Dados

### Para SQLite (desenvolvimento local)
```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Popular dados iniciais (opcional)
python manage.py shell -c "
from apps.produtos.management.commands.popular_produtos import Command
cmd = Command()
cmd.handle()
"
```

### Para Supabase (produção)
```bash
# Configurar USE_SUPABASE_DB=True no .env
# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

---

## 📁 Passo 6: Arquivos Estáticos

```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

---

## 🚀 Passo 7: Testar a Instalação

```bash
# Iniciar servidor de desenvolvimento
python manage.py runserver

# Acessar no navegador:
# http://127.0.0.1:8000/
```

### Verificações:
- [ ] Página inicial carrega
- [ ] Login funciona
- [ ] Admin panel acessível: http://127.0.0.1:8000/admin/
- [ ] Sistema de pedidos funciona

---

## 🛠️ Solução de Problemas Comuns

### Erro: "python não é reconhecido"
```bash
# Instalar Python do site oficial: python.org
# Marcar "Add to PATH" durante instalação
```

### Erro: "pip não é reconhecido"
```bash
# Reinstalar Python marcando "Add to PATH"
# Ou instalar pip manualmente
```

### Erro: Dependências não instalam
```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências uma por uma se necessário
pip install Django==5.2.4
pip install psycopg2-binary
pip install supabase
# ... continuar com outras do requirements.txt
```

### Erro: Banco de dados
```bash
# Para SQLite, verificar se o arquivo db.sqlite3 foi criado
ls -la db.sqlite3

# Para Supabase, verificar conexão
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT 1')
print('Conexão OK!')
"
```

### Erro: Módulo não encontrado
```bash
# Verificar se o ambiente virtual está ativo
# Deve aparecer (.venv) no início do prompt

# Reativar se necessário:
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

---

## 🔧 Comandos Úteis de Manutenção

```bash
# Verificar status do sistema
python manage.py check

# Ver migrações pendentes
python manage.py showmigrations

# Limpar cache
python manage.py shell -c "
from django.core.cache import cache
cache.clear()
print('Cache limpo!')
"

# Backup do banco SQLite
cp db.sqlite3 db_backup_$(date +%Y%m%d).sqlite3

# Verificar logs
tail -f server.log
```

---

## 🌐 Instalação para Produção

Se for instalar em servidor de produção:

```bash
# Usar configurações de produção
export DJANGO_SETTINGS_MODULE=DjangoProject.settings_production

# Usar Gunicorn em vez do runserver
pip install gunicorn
gunicorn DjangoProject.wsgi:application --bind 0.0.0.0:8000

# Configurar nginx como proxy reverso (opcional)
# Configurar SSL/HTTPS
# Configurar domínio
```

---

## 📞 Suporte

Se encontrar problemas:

1. **Verificar logs**: `python manage.py runserver` mostra erros
2. **Consultar CLAUDE.md**: Documentação completa do projeto
3. **Verificar requirements.txt**: Todas dependências instaladas
4. **Verificar .env**: Configurações corretas

---

**✅ INSTALAÇÃO CONCLUÍDA**

Após seguir todos os passos, o sistema estará funcionando na nova máquina!