"""
Serviço Windows para Sistema Pizzaria
Permite executar como serviço do Windows usando python-windows-service
"""

import os
import sys
import time
import subprocess
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

class PizzariaService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PizzariaSystem"
    _svc_display_name_ = "Sistema Pizzaria"
    _svc_description_ = "Servidor web do Sistema de Gestão de Pizzaria"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.process = None
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        
        # Parar o processo Django
        if self.process:
            self.process.terminate()
            
    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.main()
        
    def main(self):
        # Diretório do projeto
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Ambiente virtual
        venv_python = os.path.join(project_dir, '.venv', 'Scripts', 'python.exe')
        
        # Comando para executar Django
        cmd = [
            venv_python,
            'manage.py',
            'runserver',
            '0.0.0.0:8000',
            '--noreload',
            '--settings=settings_fast'
        ]
        
        # Iniciar processo
        self.process = subprocess.Popen(cmd)
        
        # Aguardar sinal de parada
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PizzariaService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PizzariaService)