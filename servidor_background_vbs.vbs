Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Obter diretório atual
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Mudar para o diretório do projeto
WshShell.CurrentDirectory = strPath

' Executar servidor em modo oculto
WshShell.Run "cmd /c call .venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8080", 0, False

' Script termina mas o servidor continua rodando