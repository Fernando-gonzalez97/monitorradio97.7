@echo off
echo ================================================
echo     INSTALADOR - Radio Monitor
echo ================================================
echo.

echo [1/4] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo Descargalo desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo [2/4] Creando entorno virtual...
if exist venv (
    echo Entorno virtual ya existe, saltando...
) else (
    python -m venv venv
    echo Entorno creado correctamente
)
echo.

echo [3/4] Activando entorno...
call venv\Scripts\activate.bat
echo.

echo [4/4] Instalando dependencias...
pip install --upgrade pip
pip install customtkinter
pip install requests
pip install pydub
echo.

echo ================================================
echo    INSTALACION COMPLETADA
echo ================================================
echo.
echo Para ejecutar el monitor:
echo   1. Activa el entorno: venv\Scripts\activate
echo   2. Ejecuta: python monitor.py
echo.
echo O simplemente ejecuta: iniciar.bat
echo.
pause