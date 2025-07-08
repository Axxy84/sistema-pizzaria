# Sistema Pizzaria ERP

Sistema completo de gestão para pizzarias desenvolvido com Django, Django REST Framework e Supabase.

## 📋 Funcionalidades

- **Gestão de Produtos**: Cadastro de pizzas, bebidas e outros produtos com diferentes tamanhos e preços
- **Gestão de Clientes**: Cadastro completo com múltiplos endereços
- **Sistema de Pedidos**: Controle completo do fluxo de pedidos (delivery, balcão, mesa)
- **Controle de Estoque**: Gerenciamento de ingredientes e receitas
- **Módulo Financeiro**: Controle de caixa, contas a pagar e movimentações
- **Dashboard**: Relatórios e estatísticas em tempo real
- **Autenticação**: Integrada com Supabase Auth

## 🚀 Tecnologias

- Python 3.13
- Django 5.2.4
- Django REST Framework
- Supabase (Autenticação)
- SQLite (desenvolvimento)
- PostgreSQL (produção via Supabase)

## 📦 Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositorio]
cd DjangoProject
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais do Supabase
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Execute o servidor:
```bash
python manage.py runserver
```

## 🏗️ Estrutura do Projeto

```
pizzaria_erp/
├── apps/
│   ├── authentication/    # Autenticação com Supabase
│   ├── produtos/         # Gestão de produtos e categorias
│   ├── clientes/         # Cadastro de clientes
│   ├── pedidos/          # Sistema de pedidos
│   ├── estoque/          # Controle de ingredientes
│   ├── financeiro/       # Caixa e contas
│   └── dashboard/        # Relatórios e KPIs
├── services/             # Serviços externos (Supabase)
├── templates/            # Templates HTML
├── static/              # Arquivos estáticos
└── media/               # Upload de arquivos
```

## 📚 API Endpoints

### Autenticação
- `POST /api/auth/register/` - Registro de usuário
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/user/` - Dados do usuário

### Produtos
- `GET /api/produtos/` - Listar produtos
- `POST /api/produtos/` - Criar produto
- `GET /api/produtos/categorias/` - Listar categorias
- `GET /api/produtos/tamanhos/` - Listar tamanhos

### Clientes
- `GET /api/clientes/` - Listar clientes
- `POST /api/clientes/` - Criar cliente
- `GET /api/clientes/{id}/` - Detalhes do cliente
- `POST /api/clientes/{id}/adicionar_endereco/` - Adicionar endereço

### Pedidos
- `GET /api/pedidos/` - Listar pedidos
- `POST /api/pedidos/` - Criar pedido
- `PATCH /api/pedidos/{id}/atualizar_status/` - Atualizar status
- `GET /api/pedidos/pendentes/` - Pedidos pendentes

### Estoque
- `GET /api/estoque/ingredientes/` - Listar ingredientes
- `POST /api/estoque/movimentos/` - Registrar movimento
- `GET /api/estoque/ingredientes/estoque_baixo/` - Itens com estoque baixo

### Financeiro
- `POST /api/financeiro/caixas/abrir/` - Abrir caixa
- `POST /api/financeiro/caixas/{id}/fechar/` - Fechar caixa
- `GET /api/financeiro/contas-pagar/vencidas/` - Contas vencidas
- `POST /api/financeiro/contas-pagar/{id}/pagar/` - Pagar conta

### Dashboard
- `GET /api/dashboard/` - Métricas gerais
- `GET /api/dashboard/vendas-periodo/` - Vendas por período
- `GET /api/dashboard/produtos-ranking/` - Produtos mais vendidos

## 🔒 Segurança

- Autenticação via Supabase
- CORS configurado
- CSRF protection
- Variáveis sensíveis em arquivo .env
- Row Level Security (RLS) no Supabase

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT.

## 👥 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter)

Link do Projeto: [https://github.com/seu_usuario/pizzaria_erp](https://github.com/seu_usuario/pizzaria_erp)