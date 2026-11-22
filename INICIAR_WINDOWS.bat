@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
    py -3.12 -c "import sys" >nul 2>nul
    if errorlevel 1 (
        set "PYTHON_CMD=py -3"
    ) else (
        set "PYTHON_CMD=py -3.12"
    )
) else (
    where python >nul 2>nul
    if errorlevel 1 goto sem_python
    set "PYTHON_CMD=python"
)
%PYTHON_CMD% -c "import sys; sys.exit(0 if (3,10) <= sys.version_info[:2] < (3,14) else 1)"
if errorlevel 1 goto sem_python
if not exist ".venv\Scripts\python.exe" (
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto erro
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto erro
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto erro
exit /b 0
:sem_python
echo Instale Python 3.12 em python.org e habilite Add Python to PATH.
echo Este iniciador aceita Python 3.10 a 3.13; a versao testada foi 3.12.
pause
exit /b 1
:erro
echo Nao foi possivel iniciar. Confira as mensagens acima.
pause
exit /b 1
