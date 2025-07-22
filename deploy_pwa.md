# 🚀 Guia de Deploy PWA - Sistema Pizzaria

## ✅ PWA Implementado com Sucesso!

### 📱 O que foi implementado:

1. **manifest.json** - Configurações do PWA
   - Nome, ícones, cores, atalhos
   - Modo standalone (app nativo)
   - Suporte para desktop e mobile

2. **Service Worker** - Funcionalidades offline
   - Cache inteligente de recursos
   - Página offline customizada
   - Sincronização em background
   - Push notifications

3. **Sistema de Instalação**
   - Botão de instalação automático
   - Instruções para iOS
   - Detecção de app já instalado

## 🖥️ Como Instalar em Múltiplos PCs:

### Opção 1: Deploy Local (Rede Interna)

```bash
# No PC servidor principal:
python manage.py runserver 0.0.0.0:8000

# Nos outros PCs da rede:
# Acessar: http://IP_DO_SERVIDOR:8000
# Exemplo: http://192.168.1.100:8000
```

### Opção 2: Deploy com Servidor Web (Recomendado)

1. **Instalar Nginx no servidor:**
```bash
sudo apt update
sudo apt install nginx gunicorn python3-pip
```

2. **Configurar Gunicorn:**
```bash
pip install gunicorn
gunicorn DjangoProject.wsgi:application --bind 0.0.0.0:8000
```

3. **Configurar Nginx:**
```nginx
server {
    listen 80;
    server_name pizzaria.local;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /home/labdev/Documentos/DjangoProject/staticfiles/;
    }
}
```

### Opção 3: Deploy com HTTPS (PWA Completo)

Para PWA completo com todas as funcionalidades, você precisa HTTPS:

1. **Usando Ngrok (Teste rápido):**
```bash
# Instalar ngrok
sudo snap install ngrok

# Expor aplicação
ngrok http 8000
```

2. **Certificado SSL Local (Produção):**
```bash
# Gerar certificado auto-assinado
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/pizzaria.key \
    -out /etc/ssl/certs/pizzaria.crt
```

## 📲 Instalação do PWA nos Clientes:

### Desktop (Chrome/Edge):
1. Acessar o sistema pelo navegador
2. Clicar no ícone de instalação na barra de endereços
3. Ou clicar no botão "Instalar App" que aparece
4. Confirmar instalação

### Mobile (Android):
1. Acessar o sistema pelo Chrome
2. Menu (3 pontos) → "Adicionar à tela inicial"
3. Confirmar instalação

### iOS (iPhone/iPad):
1. Acessar pelo Safari
2. Botão compartilhar → "Adicionar à Tela de Início"
3. Confirmar

## 🔧 Configurações Necessárias:

### 1. Atualizar ALLOWED_HOSTS no settings.py:
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.100',  # IP do servidor
    'pizzaria.local',  # Nome do domínio local
    '*'  # Para teste (remover em produção)
]
```

### 2. Configurar IP fixo no servidor:
```bash
# Ubuntu/Debian
sudo nano /etc/netplan/01-netcfg.yaml
```

### 3. Criar script de inicialização:
```bash
#!/bin/bash
# start_pizzaria.sh
cd /home/labdev/Documentos/DjangoProject
source .venv/bin/activate
python manage.py collectstatic --noinput
gunicorn DjangoProject.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## ✨ Funcionalidades PWA Ativas:

- ✅ **Instalável** - Ícone na área de trabalho
- ✅ **Offline** - Funciona sem internet (parcial)
- ✅ **Atualizações** - Automáticas ao reconectar
- ✅ **Notificações** - Push notifications
- ✅ **Performance** - Cache inteligente
- ✅ **Responsivo** - Desktop e mobile

## 🎯 Vantagens do PWA:

1. **Uma única instalação no servidor**
2. **Todos os PCs acessam via navegador**
3. **Atualizações instantâneas para todos**
4. **Funciona em qualquer dispositivo**
5. **Backup centralizado**
6. **Menor custo de manutenção**

## 📝 Comandos Úteis:

```bash
# Verificar IP do servidor
ip addr show

# Testar conectividade
ping IP_DO_SERVIDOR

# Reiniciar serviços
sudo systemctl restart nginx
sudo systemctl restart gunicorn

# Ver logs
tail -f /var/log/nginx/error.log
```

## 🚨 Troubleshooting:

**Problema: "Inseguro" no navegador**
- Solução: Aceitar certificado auto-assinado ou usar HTTP local

**Problema: Não aparece opção de instalar**
- Solução: Verificar se está acessando por HTTPS ou localhost

**Problema: Service Worker não registra**
- Solução: Limpar cache do navegador e recarregar

---

**🎉 Seu sistema agora é um PWA completo!**

Cada PC pode instalar como app nativo, mas todos acessam o mesmo servidor central com dados sincronizados via Supabase.