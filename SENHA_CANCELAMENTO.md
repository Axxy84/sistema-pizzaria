# Sistema de Senha para Cancelamento de Pedidos

## 📋 Visão Geral

O sistema implementa uma proteção por senha para cancelamento de pedidos, garantindo que apenas pessoas autorizadas possam cancelar pedidos no sistema.

## 🔐 Senha Atual

A senha padrão configurada é: `2024pizza`

**⚠️ IMPORTANTE: Altere esta senha antes de colocar em produção!**

## 🛠️ Como Alterar a Senha

### Método 1: Usando o Comando Django (Recomendado)

```bash
# Alterar a senha interativamente
python manage.py set_cancel_password

# Ou definir diretamente
python manage.py set_cancel_password --password "nova_senha_segura"

# Ver a senha atual
python manage.py set_cancel_password --show
```

### Método 2: Editando o settings.py

1. Abra o arquivo `DjangoProject/settings.py`
2. Localize a linha: `ADMIN_CANCEL_PASSWORD = '2024pizza'`
3. Altere para sua nova senha: `ADMIN_CANCEL_PASSWORD = 'sua_nova_senha'`
4. Salve o arquivo e reinicie o servidor

## 🔑 Métodos de Autenticação

O sistema verifica a senha em 3 níveis (nesta ordem):

1. **Senha do usuário atual** (se for superusuário)
2. **Senha configurada no settings.py** (ADMIN_CANCEL_PASSWORD)
3. **Senha de qualquer superusuário** do sistema

## 💡 Boas Práticas de Senha

- Use senhas fortes com pelo menos 8 caracteres
- Combine letras maiúsculas, minúsculas, números e símbolos
- Não use senhas óbvias como "123456" ou "admin"
- Altere a senha periodicamente
- Não compartilhe a senha desnecessariamente

## 🚀 Exemplo de Uso

1. Na lista de pedidos, clique no botão vermelho "Cancelar"
2. Um modal solicitará a senha
3. Digite a senha configurada (ou senha de admin)
4. O pedido será cancelado e marcado como "Cancelado"

## 🔧 Troubleshooting

### A senha não está funcionando
- Verifique se reiniciou o servidor após alterar a senha
- Confirme que digitou a senha corretamente (maiúsculas/minúsculas)
- Use o comando `python manage.py set_cancel_password --show` para ver a senha atual

### Esqueci a senha
- Use a senha de qualquer superusuário do Django
- Ou altere diretamente no settings.py
- Ou use o comando Django para redefinir

## 📝 Notas de Segurança

- **Produção**: NUNCA use a senha padrão em produção
- **Versionamento**: Não commite senhas reais no Git
- **Variáveis de Ambiente**: Em produção, considere usar variáveis de ambiente:

```python
# settings.py
import os
ADMIN_CANCEL_PASSWORD = os.environ.get('PIZZARIA_CANCEL_PASSWORD', 'senha_padrao')
```

## 📊 Log de Alterações

| Data | Senha | Alterado Por |
|------|-------|--------------|
| 18/07/2025 | 2024pizza | Sistema (padrão) |
| - | - | - |

---

**Última atualização**: 18/07/2025