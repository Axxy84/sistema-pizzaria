# 🖥️ Sistema Pizzaria - Versão Desktop (Electron)

## ✅ O que é isso?

Versão desktop do sistema que:
- **Instala com 1 clique** (.exe)
- **Não precisa navegador**
- **Django embutido** no app
- **Conecta no Supabase** (precisa internet)

## 📦 Como Construir o Instalador:

### 1. Instalar Node.js
```bash
# Windows: Baixar de https://nodejs.org
# Linux:
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2. Preparar o Projeto
```bash
cd electron
npm install
```

### 3. Criar Ícones
- Converter `logo.svg` para:
  - `icon.ico` (Windows) - 256x256
  - `icon.png` (Linux) - 512x512
- Sites úteis: https://convertio.co/pt/svg-ico/

### 4. Construir Instalador
```bash
# Windows (.exe)
npm run build-win

# Linux (.AppImage)
npm run build-linux
```

## 📥 Instalação no Cliente:

1. **Baixar** o arquivo `Sistema Pizzaria Setup 1.0.0.exe`
2. **Executar** e seguir instalador
3. **Abrir** pelo ícone na área de trabalho
4. **Usar** normalmente (com internet)

## 🔧 Requisitos:

- **Sistema**: Windows 10+ ou Linux
- **Internet**: Para acessar Supabase
- **RAM**: 2GB mínimo
- **Espaço**: 200MB

## ⚙️ Configurações:

O app salva configurações em:
- Windows: `%APPDATA%/pizzaria-sistema`
- Linux: `~/.config/pizzaria-sistema`

## 🐛 Problemas Comuns:

**"Erro ao conectar com banco"**
- Verificar conexão com internet
- Verificar credenciais Supabase

**"Sistema não inicia"**
- Verificar antivírus
- Executar como administrador

**"Tela branca"**
- Aguardar Django iniciar (30s)
- Verificar logs em: `%APPDATA%/pizzaria-sistema/logs`

## 📊 Vantagens:

✅ **Instalação simples** - Next, next, finish
✅ **Ícone no desktop** - Como app nativo
✅ **Menu próprio** - Atalhos rápidos
✅ **System tray** - Minimiza para bandeja
✅ **Auto-update** - Atualizações automáticas*

*Recurso futuro

## 🚀 Deploy Automático:

Para distribuir:
1. Upload do `.exe` para servidor
2. Criar página de download
3. Enviar link para clientes

---

**Suporte**: suporte@pizzaria.com