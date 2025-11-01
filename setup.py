#!/usr/bin/env python3
"""
Script de setup automatizado para instalação do projeto
Funciona em Windows, Linux e macOS
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Imprime cabeçalho do script"""
    print("=" * 60)
    print("Detector de Pessoas - Setup Automático")
    print("=" * 60)
    print()

def verificar_python():
    """Verifica se Python está instalado e na versão correta"""
    print("Verificando Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"ERRO: Python 3.7+ é necessário. Versão atual: {version.major}.{version.minor}")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} encontrado")
    return True

def criar_ambiente_virtual():
    """Cria ambiente virtual Python"""
    print("\nCriando ambiente virtual...")
    
    if os.path.exists("venv"):
        resposta = input("Ambiente virtual já existe. Recriar? (s/N): ")
        if resposta.lower() != 's':
            print("Mantendo ambiente virtual existente")
            return True
        else:
            print("Removendo ambiente virtual antigo...")
            if platform.system() == "Windows":
                subprocess.run(["rmdir", "/s", "/q", "venv"], shell=True)
            else:
                subprocess.run(["rm", "-rf", "venv"])
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Ambiente virtual criado com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("ERRO: Falha ao criar ambiente virtual")
        return False

def obter_pip():
    """Obtém caminho do pip no ambiente virtual"""
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip.exe")
        if not os.path.exists(pip_path):
            pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
    
    return pip_path

def atualizar_pip():
    """Atualiza pip no ambiente virtual"""
    print("\nAtualizando pip...")
    pip_path = obter_pip()
    
    try:
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        print("✓ pip atualizado")
        return True
    except subprocess.CalledProcessError:
        print("AVISO: Falha ao atualizar pip, continuando...")
        return True

def instalar_dependencias():
    """Instala dependências do requirements.txt"""
    print("\nInstalando dependências...")
    pip_path = obter_pip()
    
    if not os.path.exists("requirements.txt"):
        print("ERRO: requirements.txt não encontrado")
        return False
    
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("ERRO: Falha ao instalar dependências")
        return False

def verificar_instalacao():
    """Verifica se OpenCV foi instalado corretamente"""
    print("\nVerificando instalação...")
    
    # Caminho do Python no ambiente virtual
    if platform.system() == "Windows":
        python_path = os.path.join("venv", "Scripts", "python.exe")
        if not os.path.exists(python_path):
            python_path = os.path.join("venv", "Scripts", "python")
    else:
        python_path = os.path.join("venv", "bin", "python")
    
    try:
        resultado = subprocess.run(
            [python_path, "-c", "import cv2; print(cv2.__version__)"],
            capture_output=True,
            text=True,
            check=True
        )
        versao = resultado.stdout.strip()
        print(f"✓ OpenCV {versao} instalado corretamente")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("AVISO: Não foi possível verificar OpenCV")
        return False

def mostrar_comandos():
    """Mostra comandos para usar o projeto"""
    print("\n" + "=" * 60)
    print("Instalação concluída!")
    print("=" * 60)
    print("\nPara usar o projeto:\n")
    
    if platform.system() == "Windows":
        print("1. Ative o ambiente virtual:")
        print("   venv\\Scripts\\Activate.ps1")
        print("\n2. Execute um detector:")
        print("   python detector_circulos_centro.py")
        print("   python detector_basico.py")
        print("   python detector_avancado.py")
    else:
        print("1. Ative o ambiente virtual:")
        print("   source venv/bin/activate")
        print("\n2. Execute um detector:")
        print("   python3 detector_circulos_centro.py")
        print("   python3 detector_basico.py")
        print("   python3 detector_avancado.py")
    
    print("\nPara desativar o ambiente virtual:")
    print("   deactivate")
    print("\n" + "=" * 60)

def main():
    """Função principal"""
    print_header()
    
    # Verificar Python
    if not verificar_python():
        sys.exit(1)
    
    # Criar ambiente virtual
    if not criar_ambiente_virtual():
        sys.exit(1)
    
    # Atualizar pip
    atualizar_pip()
    
    # Instalar dependências
    if not instalar_dependencias():
        sys.exit(1)
    
    # Verificar instalação
    verificar_instalacao()
    
    # Mostrar comandos
    mostrar_comandos()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\nERRO: {e}")
        sys.exit(1)

