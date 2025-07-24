# 📋 GUIA DE INSTALAÇÃO - SISTEMA PIZZARIA

## 🎯 Requisitos do Sistema

### Mínimos:
- **Sistema Operacional**: Windows 10/11 (64 bits)
- **Processador**: Intel Core i3 ou equivalente
- **Memória RAM**: 4GB
- **Espaço em Disco**: 2GB livres
- **Python**: 3.10 ou superior
- **Conexão com Internet**: Para instalação inicial

### Recomendados:
- **Processador**: Intel Core i5 ou equivalente
- **Memória RAM**: 8GB
- **SSD**: Para melhor performance
- **Monitor**: Resolução mínima 1366x768

## 📦 Instalação Passo a Passo

### 1. Preparação do Ambiente

1. **Instalar Python** (se não tiver):
   - Baixe em: https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE**: Marque a opção "Add Python to PATH" durante a instalação
   - Versão recomendada: Python 3.11 ou 3.12

2. **Extrair arquivos do sistema**:
   - Descompacte o arquivo ZIP em `C:\SistemaPizzaria` (recomendado)
   - Evite caminhos com espaços ou caracteres especiais

### 2. Instalação Automática

1. **Abra o Windows Explorer** e navegue até a pasta do sistema
2. **Execute como Administrador**: `instalar_windows.bat`
3. O instalador irá automaticamente:
   - ✅ Verificar Python
   - ✅ Criar ambiente virtual
   - ✅ Instalar todas as dependências
   - ✅ Configurar banco de dados
   - ✅ Criar estrutura de pastas
   - ✅ Aplicar migrações
   - ✅ Coletar arquivos estáticos

4. **Criar usuário administrador**:
   - Quando solicitado, digite `S` para criar
   - Defina um usuário e senha seguros
   - Guarde essas credenciais!

### 3. Configuração do Banco de Dados

O sistema está configurado para usar **SQLite** (banco local) por padrão.

Para usar **PostgreSQL/Supabase**:
1. Edite o arquivo `.env`
2. Configure as variáveis:
   ```
   USE_SUPABASE_DB=True
   DATABASE_URL=sua_url_do_supabase
   ```

### 4. Iniciar o Sistema

1. **Execute**: `iniciar_pizzaria.bat`
2. O servidor iniciará em: http://localhost:8000
3. Acesse pelo navegador (Chrome/Edge recomendado)

### 5. Configuração Inicial

1. **Acesse o admin**: http://localhost:8000/admin
2. **Configure**:
   - Categorias de produtos
   - Produtos do cardápio
   - Dados da empresa
   - Formas de pagamento

## 🔧 Scripts Disponíveis

- `instalar_windows.bat` - Instalação completa
- `iniciar_pizzaria.bat` - Iniciar servidor
- `ATUALIZAR.bat` - Atualizar sistema
- `criar_atalhos.bat` - Criar atalhos na área de trabalho
- `instalar_servico.bat` - Instalar como serviço Windows
- `run_no_auth.bat` - Modo sem autenticação (desenvolvimento)

## ⚡ Otimizações de Performance

O sistema inclui configurações otimizadas:
- Cache Redis (opcional)
- Compressão GZIP
- Arquivos estáticos via WhiteNoise
- Banco de dados otimizado

## 🛠️ Solução de Problemas

### Python não encontrado:
- Reinstale Python marcando "Add to PATH"
- Reinicie o computador após instalar

### Erro de permissão:
- Execute sempre como Administrador
- Verifique antivírus/firewall

### Porta 8000 em uso:
- Edite `iniciar_pizzaria.bat`
- Mude para outra porta (ex: 8080)

### Erro de migração:
```batch
python manage.py migrate --run-syncdb
```

## 📱 Acesso Mobile

O sistema é totalmente responsivo:
1. No celular, acesse: http://IP_DO_COMPUTADOR:8000
2. Para descobrir o IP: `ipconfig` no CMD
3. Exemplo: http://192.168.1.100:8000

## 🔒 Segurança

1. **Mude a SECRET_KEY** em produção
2. **Configure HTTPS** para acesso externo
3. **Firewall**: Libere apenas porta necessária
4. **Backup regular** do banco de dados

## 📞 Suporte

Em caso de problemas:
1. Verifique os logs em `/logs`
2. Execute: `python manage.py check`
3. Consulte a documentação em `/docs`

## ✅ Checklist Pós-Instalação

- [ ] Sistema instalado e funcionando
- [ ] Usuário admin criado
- [ ] Produtos cadastrados
- [ ] Configurações da empresa
- [ ] Teste de pedido completo
- [ ] Backup configurado
- [ ] Atalhos criados

---

**Versão**: 2.0  
**Última atualização**: Janeiro 2025