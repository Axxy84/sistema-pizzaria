# 🚀 Como Rodar e Testar o Projeto

## 1️⃣ Ativar o Ambiente Virtual

```bash
# Se você estiver fora do ambiente virtual, ative-o:
source .venv/bin/activate
```

## 2️⃣ Instalar Dependências (se necessário)

```bash
# Instalar todas as dependências do projeto
pip install -r requirements.txt
```

## 3️⃣ Configurar Variáveis de Ambiente

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` e adicione suas credenciais do Supabase:
```
SUPABASE_URL=sua_url_aqui
SUPABASE_ANON_KEY=sua_chave_anon_aqui
SUPABASE_SERVICE_KEY=sua_chave_service_aqui
```

## 4️⃣ Executar Migrações (se necessário)

```bash
python manage.py migrate
```

## 5️⃣ Rodar o Servidor

```bash
python manage.py runserver
```

O servidor iniciará em: http://localhost:8000/

## 6️⃣ Páginas para Testar

### 🏠 Homepage
- **URL**: http://localhost:8000/
- **O que testar**: Página inicial com links para login/registro

### 🔐 Registro de Usuário
- **URL**: http://localhost:8000/auth/register/
- **Como testar**:
  1. Acesse a página
  2. Preencha email e senha
  3. Clique em "Registrar"
  4. Se bem-sucedido, será redirecionado para login

### 🔑 Login
- **URL**: http://localhost:8000/auth/login/
- **Como testar**:
  1. Use as credenciais criadas no registro
  2. Clique em "Entrar"
  3. Se bem-sucedido, será redirecionado para home

### 🚪 Logout
- **URL**: http://localhost:8000/auth/logout/
- **O que acontece**: Encerra a sessão e redireciona para home

### 🛠️ Admin Django
- **URL**: http://localhost:8000/admin/
- **Nota**: Requer superusuário Django (não Supabase)

## 7️⃣ Criar Superusuário (Opcional)

Para acessar o admin do Django:
```bash
python manage.py createsuperuser
```

## 🧪 Comandos Úteis para Debug

```bash
# Verificar se há problemas
python manage.py check

# Ver status das migrations
python manage.py showmigrations

# Console interativo Django
python manage.py shell
```

## 📱 Testar no Console do Navegador

Abra o console (F12) e você verá mensagens de debug quando fizer login/logout.

## ⚠️ Problemas Comuns

1. **Erro de conexão com Supabase**: Verifique as credenciais no `.env`
2. **Página não carrega**: Certifique-se que o servidor está rodando
3. **Erro 500**: Verifique os logs no terminal onde o servidor está rodando

## 🎯 Fluxo de Teste Completo

1. Acesse http://localhost:8000/
2. Clique em "Registrar"
3. Crie uma conta nova
4. Faça login com a conta criada
5. Navegue pela home (verá mensagem de boas-vindas)
6. Faça logout
7. Tente acessar novamente (verá que não está mais logado)