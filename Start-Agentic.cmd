@echo off
cd /d "%~dp0"
if not exist "Agentic Studio.exe" powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0desktop\build.ps1"
if not exist "Agentic Studio.exe" exit /b 1
start "" "%~dp0Agentic Studio.exe"
