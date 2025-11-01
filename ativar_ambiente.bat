@echo off
echo ========================================
echo Ativando ambiente virtual...
echo ========================================
call venv\Scripts\activate.bat

echo.
echo Ambiente virtual ativado!
echo.
echo Para instalar as dependencias, execute:
echo   pip install -r requirements.txt
echo.
echo Para desativar o ambiente virtual:
echo   deactivate
echo.

cmd /k

