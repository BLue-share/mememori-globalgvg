@echo off

:: カレントディレクトリを取得してPowerShellスクリプトに渡す
set CURRENT_DIR=%cd%

:: PowerShellスクリプトを実行し、カレントディレクトリを引数として渡す
powershell -ExecutionPolicy Bypass -File start_servers.ps1 "%CURRENT_DIR%"

exit
