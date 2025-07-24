' Script VBScript para iniciar o servidor Django minimizado
' Útil para adicionar na pasta Inicializar do Windows

Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Obtém o diretório do script
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Muda para o diretório do projeto
WshShell.CurrentDirectory = strPath

' Inicia o servidor minimizado e sem janela de comando visível
WshShell.Run "cmd /c run_forever.bat", 0, False

' Mensagem opcional (comente se não quiser)
' MsgBox "Servidor Django iniciado em segundo plano!", vbInformation, "Django Server"