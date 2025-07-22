const { app, BrowserWindow, Menu, Tray, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const isDev = require('electron-is-dev');
const Store = require('electron-store');

// Store para configurações
const store = new Store();

let mainWindow;
let djangoProcess;
let tray;

// Porta do Django
const DJANGO_PORT = 8765;
const DJANGO_URL = `http://127.0.0.1:${DJANGO_PORT}`;

// Função para iniciar o Django
function startDjango() {
  return new Promise((resolve, reject) => {
    const djangoPath = isDev 
      ? path.join(__dirname, '..') 
      : path.join(process.resourcesPath, 'django');
    
    const pythonPath = isDev 
      ? path.join(djangoPath, '.venv', 'bin', 'python')
      : path.join(djangoPath, '.venv', 'Scripts', 'python.exe');
    
    const managePath = path.join(djangoPath, 'manage.py');
    
    console.log('Iniciando Django em:', djangoPath);
    
    // Inicia o processo Django
    djangoProcess = spawn(pythonPath, [
      managePath, 
      'runserver', 
      `127.0.0.1:${DJANGO_PORT}`,
      '--noreload'
    ], {
      cwd: djangoPath,
      env: {
        ...process.env,
        PYTHONUNBUFFERED: '1',
        USE_SUPABASE_DB: 'True'
      }
    });

    djangoProcess.stdout.on('data', (data) => {
      console.log(`Django: ${data}`);
      if (data.toString().includes('Starting development server')) {
        setTimeout(() => resolve(), 2000); // Aguarda 2s para garantir
      }
    });

    djangoProcess.stderr.on('data', (data) => {
      console.error(`Django Error: ${data}`);
    });

    djangoProcess.on('error', (error) => {
      console.error('Erro ao iniciar Django:', error);
      reject(error);
    });

    // Timeout de 30 segundos
    setTimeout(() => {
      reject(new Error('Timeout ao iniciar Django'));
    }, 30000);
  });
}

// Função para verificar se Django está rodando
async function waitForDjango() {
  const maxAttempts = 30;
  let attempts = 0;
  
  while (attempts < maxAttempts) {
    try {
      const response = await fetch(DJANGO_URL);
      if (response.ok) {
        console.log('Django está pronto!');
        return true;
      }
    } catch (error) {
      // Django ainda não está pronto
    }
    
    attempts++;
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  return false;
}

// Criar janela principal
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 600,
    icon: path.join(__dirname, 'icon.ico'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    show: false, // Não mostrar até estar pronto
    titleBarStyle: 'default',
    backgroundColor: '#f9fafb'
  });

  // Menu customizado
  const menu = Menu.buildFromTemplate([
    {
      label: 'Sistema',
      submenu: [
        { label: 'Recarregar', role: 'reload', accelerator: 'F5' },
        { label: 'Tela Cheia', role: 'togglefullscreen', accelerator: 'F11' },
        { type: 'separator' },
        { label: 'Sair', role: 'quit', accelerator: 'Ctrl+Q' }
      ]
    },
    {
      label: 'Navegação',
      submenu: [
        { 
          label: 'Dashboard', 
          click: () => mainWindow.loadURL(DJANGO_URL),
          accelerator: 'Ctrl+D'
        },
        { 
          label: 'Produtos', 
          click: () => mainWindow.loadURL(`${DJANGO_URL}/produtos/`),
          accelerator: 'Ctrl+P'
        },
        { 
          label: 'Pedidos', 
          click: () => mainWindow.loadURL(`${DJANGO_URL}/pedidos/`),
          accelerator: 'Ctrl+O'
        },
        { 
          label: 'Clientes', 
          click: () => mainWindow.loadURL(`${DJANGO_URL}/clientes/`),
          accelerator: 'Ctrl+C'
        }
      ]
    },
    {
      label: 'Ajuda',
      submenu: [
        { 
          label: 'Suporte', 
          click: () => shell.openExternal('https://suporte.pizzaria.com')
        },
        { 
          label: 'Sobre', 
          click: () => {
            const { dialog } = require('electron');
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Sobre',
              message: 'Sistema de Gestão - Pizzaria',
              detail: 'Versão 1.0.0\nDesenvolvido com Django + Electron\nBanco de dados: Supabase',
              buttons: ['OK']
            });
          }
        }
      ]
    }
  ]);
  
  Menu.setApplicationMenu(menu);

  // Mostrar quando pronto
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Eventos da janela
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Prevenir links externos de abrir na janela
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('http') && !url.includes('127.0.0.1')) {
      shell.openExternal(url);
      return { action: 'deny' };
    }
    return { action: 'allow' };
  });
}

// System tray
function createTray() {
  tray = new Tray(path.join(__dirname, 'icon.ico'));
  
  const contextMenu = Menu.buildFromTemplate([
    { label: 'Abrir', click: () => mainWindow.show() },
    { label: 'Minimizar', click: () => mainWindow.minimize() },
    { type: 'separator' },
    { label: 'Sair', click: () => app.quit() }
  ]);
  
  tray.setToolTip('Sistema Pizzaria');
  tray.setContextMenu(contextMenu);
  
  tray.on('click', () => {
    mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
  });
}

// App events
app.whenReady().then(async () => {
  console.log('Electron pronto, iniciando Django...');
  
  try {
    // Mostrar splash screen
    const splash = new BrowserWindow({
      width: 400,
      height: 300,
      frame: false,
      alwaysOnTop: true,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false
      }
    });
    
    splash.loadFile(path.join(__dirname, 'splash.html'));
    
    // Iniciar Django
    await startDjango();
    await waitForDjango();
    
    // Criar janela principal
    createWindow();
    createTray();
    
    // Carregar aplicação
    mainWindow.loadURL(DJANGO_URL);
    
    // Fechar splash
    setTimeout(() => splash.close(), 1000);
    
  } catch (error) {
    console.error('Erro ao iniciar:', error);
    const { dialog } = require('electron');
    dialog.showErrorBox('Erro', `Não foi possível iniciar o sistema: ${error.message}`);
    app.quit();
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Limpar ao fechar
app.on('before-quit', () => {
  if (djangoProcess) {
    console.log('Encerrando Django...');
    djangoProcess.kill();
  }
});