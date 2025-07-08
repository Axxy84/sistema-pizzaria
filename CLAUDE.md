# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django 5.2.4 project using Python 3.13 with a virtual environment at `.venv/`.

## Common Commands

### Development Server
```bash
python manage.py runserver
```

### Database Management
```bash
python manage.py makemigrations  # Create new migrations
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin user
```

### Django Shell
```bash
python manage.py shell           # Interactive Python shell with Django loaded
```

### Static Files
```bash
python manage.py collectstatic   # Collect static files for production
```

### Testing
```bash
python manage.py test            # Run all tests
python manage.py test app_name   # Run tests for specific app
```

## Project Structure

```
DjangoProject/
├── DjangoProject/           # Main project configuration
│   ├── settings.py         # Django settings (SQLite DB, DEBUG=True)
│   ├── urls.py            # URL routing (currently only admin)
│   ├── wsgi.py            # WSGI deployment config
│   └── asgi.py            # ASGI deployment config
├── manage.py               # Django management commands
├── templates/              # Project-level templates directory
└── .venv/                  # Python virtual environment
```

## Key Configuration

- **Database**: Supabase PostgreSQL (pooler IPv4) - configurado para `USE_SUPABASE_DB=True`
- **Templates**: Configured to use `/templates/` directory  
- **Installed Apps**: Django defaults + REST framework + CORS + custom apps (authentication, produtos, pedidos, clientes, estoque, financeiro, dashboard)
- **DEBUG**: True (development mode)

## Database Configuration

### Supabase Connection
- **Host**: `aws-0-sa-east-1.pooler.supabase.com` (pooler IPv4)
- **User**: `postgres.aewcurtmikqelqykpqoa` 
- **Database**: `postgres`
- **Port**: `5432`
- **SSL**: Required

### Connection Issues Resolution
Se houver problemas de conectividade IPv6, use o pooler do Supabase:
- Configure `DATABASE_HOST=aws-0-sa-east-1.pooler.supabase.com`
- Use formato de usuário: `postgres.{project_ref}`
- Mantenha `sslmode=require` na connection string

### Toggle Database
Para alternar entre SQLite e Supabase:
```bash
# Para usar Supabase
USE_SUPABASE_DB=True

# Para usar SQLite local
USE_SUPABASE_DB=False
```

## Creating New Django Apps

To add functionality, create Django apps:
```bash
python manage.py startapp app_name
```

Then add to `INSTALLED_APPS` in settings.py.

## Dependencies

Current dependencies (should be saved to requirements.txt):
- Django==5.2.4
- asgiref==3.9.0
- sqlparse==0.5.3

To create requirements.txt:
```bash
pip freeze > requirements.txt
```


. **Planejamento antes de agir**  
   Primeiro, pense no problema. Leia a base de código para encontrar os arquivos relevantes e escreva um plano no arquivo `tasks/todo.md`.

2. **Tarefas rastreáveis**  
   O plano deve conter uma **lista de tarefas marcáveis** (`[ ]` ou `- [ ]`) para acompanhar o progresso.

3. **Validação antes da execução**  
   Antes de iniciar o trabalho, **entre em contato comigo**. Eu irei revisar e aprovar o plano.

4. **Execução iterativa com rastreamento**  
   Execute as tarefas **uma a uma**, marcando como concluídas conforme avança (`[x]` ou `- [x]`).

5. **Transparência total nas mudanças**  
   A cada passo, me forneça **uma explicação detalhada das alterações feitas** no código.

6. **Mantenha simples**  
   Cada tarefa e mudança de código deve ser **a menor unidade possível**. Evite alterações grandes ou complexas. O impacto no sistema deve ser mínimo.  
   > Tudo se resume à **simplicidade**.

7. **Documentação e revisão final**  
   Ao final, adicione uma seção de **revisão no `todo.md`** com:
   - Resumo das alterações realizadas
   - Observações relevantes
   - Pontos de atenção para revisões futuras

---

## 🚨 Aviso de Segurança

Antes de finalizar:

- Revise cuidadosamente todo o código recém-escrito.  
- Verifique aderência às **boas práticas de segurança**.  
- **Remova qualquer informação sensível** e proteja contra vulnerabilidades.

---

## 🧠 Aprendizado com o Claude

Após cada modificação:

- Explique em detalhes a **funcionalidade criada**.
- Descreva o que foi alterado e **como o código funciona**.
- Aja como um engenheiro sênior explicando para um júnior.

---

## 🧘 Seja produtivo enquanto o Claude cozinha

Durante os intervalos em que a IA está pensando ou processando:

- Use o tempo para **gerar novas ideias**, **refletir sobre negócios** ou **explorar conteúdos estratégicos**.
- Evite se distrair.  
- Use este espaço de chat como um **laboratório mental**.

> 💡 **Como podemos usar melhor esse tempo juntos?**  
> Podemos explorar ideias de produtos, validar hipóteses, desenhar estratégias ou até aprofundar em tecnologias que você queira dominar.