Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\build-release"
WshShell.Run "cmd /c ..\JUGAR_ACE_COMBAT_2.bat", 0, False
