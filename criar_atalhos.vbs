' Script VBScript para criar atalhos na área de trabalho
Option Explicit

Dim objShell, objDesktop, objLink
Dim strDesktop, strProjectPath

Set objShell = CreateObject("WScript.Shell")
strDesktop = objShell.SpecialFolders("Desktop")
strProjectPath = objShell.CurrentDirectory

' Criar atalho para iniciar o sistema
Set objLink = objShell.CreateShortcut(strDesktop & "\Sistema Pizzaria.lnk")
objLink.TargetPath = strProjectPath & "\iniciar_pizzaria.bat"
objLink.WorkingDirectory = strProjectPath
objLink.IconLocation = "C:\Windows\System32\shell32.dll, 13"
objLink.Description = "Iniciar Sistema Pizzaria"
objLink.Save

' Criar atalho para o navegador
Set objLink = objShell.CreateShortcut(strDesktop & "\Pizzaria - Navegador.lnk")
objLink.TargetPath = "http://localhost:8000"
objLink.IconLocation = "C:\Windows\System32\shell32.dll, 14"
objLink.Description = "Abrir Sistema Pizzaria no Navegador"
objLink.Save

WScript.Echo "Atalhos criados com sucesso na área de trabalho!"