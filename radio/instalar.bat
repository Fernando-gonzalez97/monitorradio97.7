@echo off
echo ================================================
echo      Radio Monitor - Iniciando...
echo ================================================
echo.

if not exist venv (
    echo ERROR: Entorno virtual no encontrado
    echo Ejecuta primero: instalar.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python monitor.py

pause