# 🚀 Guia Completo - Servidor Django Sempre Rodando no Windows

Este guia explica todas as opções para manter o servidor Django rodando permanentemente no Windows.

## 📋 Opções Disponíveis

### 1. **run_forever.bat** (Mais Simples)
Script que mantém o servidor rodando com auto-restart em caso de falha.

**Como usar:**
```batch
run_forever.bat
```

**Características:**
- ✅ Reinicia automaticamente se o servidor parar
- ✅ Mantém logs de todas as sessões
- ✅ Mostra status na tela
- ❌ Precisa deixar janela aberta

---

### 2. **run_service.bat** (Intermediário)
Sistema de serviço com menu interativo e monitoramento.

**Como usar:**
```batch
run_service.bat
```

**Menu de opções:**
1. Iniciar Serviço
2. Status do Serviço  
3. Parar Serviço
4. Ver Logs
5. Configurações

**Características:**
- ✅ Monitor em background
- ✅ Interface com menu
- ✅ Logs organizados
- ❌ Não inicia com Windows

---

### 3. **create_scheduled_task.bat** (Recomendado) 
Cria tarefa agendada do Windows que inicia automaticamente.

**Como usar:**
```batch
# Executar como Administrador
create_scheduled_task.bat
```

**Características:**
- ✅ Inicia automaticamente com Windows
- ✅ Reinicia se o servidor parar
- ✅ Não precisa deixar janela aberta
- ✅ Integrado ao Windows
- ✅ Fácil de gerenciar

---

### 4. **install_windows_service.bat** (Profissional)
Instala como serviço real do Windows usando NSSM.

**Pré-requisito:**
1. Baixar NSSM: https://nssm.cc/download
2. Extrair `nssm.exe` (64-bit) para pasta `tools/`

**Como usar:**
```batch
# Executar como Administrador
install_windows_service.bat
```

**Características:**
- ✅ Serviço nativo do Windows
- ✅ Inicia antes do login
- ✅ Gerenciamento profissional
- ✅ Logs rotativos
- ❌ Requer NSSM

---

### 5. **start_minimized.vbs** (Inicialização Automática)
Script VBS para adicionar na pasta Inicializar.

**Como configurar:**
1. Pressione `Win + R`
2. Digite `shell:startup`
3. Copie `start_minimized.vbs` para esta pasta

**Características:**
- ✅ Inicia com Windows
- ✅ Sem janela visível
- ✅ Simples de configurar
- ❌ Só funciona após login

---

## 🎯 Qual Escolher?

### Para desenvolvimento local:
→ Use **run_forever.bat**

### Para produção em PC dedicado:
→ Use **create_scheduled_task.bat**

### Para servidor profissional:
→ Use **install_windows_service.bat**

### Para PC pessoal com auto-start:
→ Use **start_minimized.vbs**

---

## 🛠️ Scripts Auxiliares

- **stop_server.bat** - Para o servidor
- **server_status.bat** - Verifica status
- **view_logs.bat** - Visualiza logs

---

## 📊 Monitoramento

### Verificar se está rodando:
```batch
server_status.bat
```

### Ver logs em tempo real:
```batch
# Navegar até pasta logs
cd logs\forever
type server_*.log
```

### Testar conexão:
```batch
curl http://localhost:8080
```

---

## 🔧 Solução de Problemas

### Servidor não inicia:
1. Verifique se a porta 8080 está livre
2. Verifique o ambiente virtual (.venv)
3. Veja os logs de erro

### Para matar todos os processos:
```batch
stop_server.bat
```

### Limpar portas travadas:
```batch
# Como administrador
netstat -ano | findstr :8080
taskkill /F /PID [numero_do_pid]
```

---

## 🚨 Dicas Importantes

1. **Firewall**: Libere a porta 8080 no Windows Firewall
2. **Antivírus**: Adicione exceção para a pasta do projeto
3. **Energia**: Configure para nunca suspender o PC
4. **Atualizações**: Desative reinicialização automática

---

## 📱 Acesso Remoto

Para acessar de outros dispositivos na rede:
1. Descubra o IP do PC: `ipconfig`
2. Acesse: `http://[SEU-IP]:8080`
3. Configure firewall para permitir

---

## 💡 Comando Rápido

Para usuários avançados, adicione ao PATH e use:
```batch
django-server start
django-server stop
django-server status
```

Criando arquivo `django-server.bat` na pasta System32.