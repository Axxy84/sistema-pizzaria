# 🍕 Guia de Instalação - Sistema Pizzaria para Windows

## 📋 Pré-requisitos

1. **Python 3.10 ou superior** instalado
   - Download: https://www.python.org/downloads/
   - Durante instalação, marque "Add Python to PATH"

2. **Windows 10/11** (64-bit)

## 🚀 Instalação Rápida

### Opção 1: Instalação Simples (Recomendado)

1. **Baixe o projeto** para uma pasta (ex: `C:\Pizzaria`)

2. **Execute o instalador:**
   ```
   instalar_windows.bat
   ```
   Este script irá:
   - ✅ Criar ambiente virtual Python
   - ✅ Instalar todas as dependências
   - ✅ Configurar o banco de dados
   - ✅ Preparar arquivos estáticos

3. **Crie os atalhos na área de trabalho:**
   ```
   criar_atalhos.bat
   ```

4. **Inicie o sistema:**
   - Clique no atalho "Sistema Pizzaria" na área de trabalho
   - Ou execute: `iniciar_pizzaria.bat`

5. **Acesse o sistema:**
   - Abra o navegador em: http://localhost:8000
   - Ou clique no atalho "Pizzaria - Navegador"

### Opção 2: Instalação como Serviço Windows

Para que o sistema inicie automaticamente com o Windows:

1. **Execute como Administrador:**
   ```
   instalar_servico.bat
   ```

2. **Comandos úteis do serviço:**
   ```batch
   :: Parar o serviço
   net stop PizzariaSystem
   
   :: Iniciar o serviço
   net start PizzariaSystem
   
   :: Verificar status
   sc query PizzariaSystem
   
   :: Remover o serviço
   python pizzaria_service.py remove
   ```

## 📁 Estrutura de Arquivos

```
C:\Pizzaria\
├── instalar_windows.bat      # Instalador principal
├── iniciar_pizzaria.bat      # Iniciar servidor
├── criar_atalhos.bat         # Criar atalhos
├── instalar_servico.bat      # Instalar como serviço
├── run_fast.py              # Script Python otimizado
├── settings_fast.py         # Configurações otimizadas
└── db.sqlite3               # Banco de dados
```

## ⚡ Características da Versão Otimizada

- **Sem autenticação** - Acesso direto ao sistema
- **Performance máxima** - Cache em memória, queries otimizadas
- **Banco SQLite** - Sem dependências externas
- **Interface responsiva** - Funciona em qualquer dispositivo

## 🛠️ Solução de Problemas

### Python não encontrado
- Reinstale Python marcando "Add to PATH"
- Ou adicione manualmente: `C:\Python310` ao PATH

### Porta 8000 em uso
Edite `iniciar_pizzaria.bat` e mude a porta:
```batch
python manage.py runserver 0.0.0.0:8080
```

### Erro de permissão
- Execute os arquivos .bat como Administrador
- Ou mova o projeto para `C:\` ao invés de `Program Files`

### Sistema não inicia
1. Verifique se o ambiente virtual foi criado: `.venv\`
2. Reinstale as dependências:
   ```
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🔧 Configurações Avançadas

### Mudar porta padrão
Edite `settings_fast.py`:
```python
ALLOWED_HOSTS = ['*']  # Permite acesso de qualquer IP
```

### Habilitar debug
Em `settings_fast.py`:
```python
DEBUG = True  # Já está habilitado por padrão
```

### Backup do banco
Copie regularmente o arquivo `db.sqlite3`

## 📱 Acesso pela Rede Local

Para acessar de outros dispositivos na mesma rede:

1. Descubra o IP do computador:
   ```
   ipconfig
   ```

2. Acesse de outro dispositivo:
   ```
   http://192.168.1.100:8000
   ```

## 🆘 Suporte

Em caso de problemas:
1. Verifique o arquivo de log em `logs\`
2. Execute em modo debug: `python manage.py runserver --verbosity 3`
3. Verifique se todas as dependências foram instaladas

## ✅ Checklist Pós-Instalação

- [ ] Sistema acessível em http://localhost:8000
- [ ] Dashboard carregando corretamente
- [ ] Atalhos criados na área de trabalho
- [ ] Produtos e pedidos funcionando
- [ ] Performance rápida e responsiva

---

**Versão**: 1.0 - Otimizada para Performance
**Última atualização**: Janeiro 2025