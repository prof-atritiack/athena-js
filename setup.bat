@echo off
echo ========================================
echo Configurando ambiente do projeto
echo ========================================
echo.

REM Verifica se o ambiente virtual existe
if not exist "venv\" (
    echo Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERRO: Nao foi possivel criar o ambiente virtual
        pause
        exit /b 1
    )
    echo Ambiente virtual criado com sucesso!
) else (
    echo Ambiente virtual ja existe.
)

echo.
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERRO: Nao foi possivel instalar as dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo Configuracao concluida!
echo ========================================
echo.
echo Ambiente virtual ativado e dependencias instaladas.
echo.
echo Para executar os scripts:
echo   python teste_camera.py
echo   python detector_basico.py
echo   python detector_avancado.py
echo.
echo Para desativar o ambiente virtual:
echo   deactivate
echo.

cmd /k

