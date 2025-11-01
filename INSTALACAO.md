# Guia de Instalação - Nova Máquina

Este guia fornece instruções passo a passo para instalar e configurar o projeto em uma nova máquina.

## Pré-requisitos

### Sistema Operacional
- Windows 10/11, Linux (Ubuntu/Debian), ou macOS

### Software Necessário
1. **Python 3.7 ou superior**
   - Verificar instalação: `python --version` ou `python3 --version`
   - Download: https://www.python.org/downloads/
   - Durante instalação no Windows: marcar "Add Python to PATH"

2. **Git** (para clonar o repositório)
   - Verificar instalação: `git --version`
   - Download: https://git-scm.com/downloads

3. **Webcam/Câmera**
   - Câmera USB ou câmera integrada do notebook

## Instalação Passo a Passo

### 1. Clonar o Repositório

**Via Git:**
```bash
git clone <URL_DO_REPOSITORIO>
cd athena-js
```

**Ou baixar e extrair o arquivo ZIP:**
- Baixar o projeto
- Extrair para uma pasta
- Abrir terminal na pasta do projeto

### 2. Verificar Python

**Windows (PowerShell ou CMD):**
```powershell
python --version
```
Deve mostrar: `Python 3.7.x` ou superior

**Linux/Mac:**
```bash
python3 --version
```
Deve mostrar: `Python 3.7.x` ou superior

Se não estiver instalado ou versão inferior a 3.7:
- Baixar Python em: https://www.python.org/downloads/
- Windows: marcar opção "Add Python to PATH" durante instalação

### 3. Criar Ambiente Virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
```

**Linux/Mac:**
```bash
python3 -m venv venv
```

Isso cria uma pasta `venv` com um ambiente Python isolado.

### 4. Ativar Ambiente Virtual

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

Se der erro de política de execução:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Após ativar, você verá `(venv)` no início da linha do terminal.

### 5. Atualizar pip (Recomendado)

**Windows:**
```powershell
python -m pip install --upgrade pip
```

**Linux/Mac:**
```bash
python3 -m pip install --upgrade pip
```

### 6. Instalar Dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

Isso instalará:
- opencv-python (OpenCV para Python)
- numpy (Biblioteca numérica)

Tempo estimado: 2-5 minutos (dependendo da conexão de internet)

### 7. Verificar Instalação

Teste se o OpenCV foi instalado corretamente:

**Windows:**
```powershell
python -c "import cv2; print(f'OpenCV versão: {cv2.__version__}')"
```

**Linux/Mac:**
```bash
python3 -c "import cv2; print(f'OpenCV versão: {cv2.__version__}')"
```

Deve mostrar algo como: `OpenCV versão: 4.x.x`

### 8. Testar Câmera

Teste se a câmera está acessível:

**Windows:**
```powershell
python -c "import cv2; cap = cv2.VideoCapture(0); print('Câmera OK!' if cap.isOpened() else 'Câmera não encontrada'); cap.release()"
```

**Linux/Mac:**
```bash
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Câmera OK!' if cap.isOpened() else 'Câmera não encontrada'); cap.release()"
```

## Executar os Detectores

Com o ambiente virtual ativado:

### Detector de Círculos (Recomendado para câmera acima)
```bash
python detector_circulos_centro.py
```

### Detector Básico (Pessoas completas)
```bash
python detector_basico.py
```

### Detector Avançado (Pessoas completas)
```bash
python detector_avancado.py
```

## Solução de Problemas Comuns

### Erro: "python não é reconhecido como comando"

**Windows:**
- Verificar se Python está no PATH
- Reinstalar Python marcando "Add Python to PATH"
- Tentar `py` em vez de `python`

**Linux:**
- Usar `python3` em vez de `python`
- Instalar Python: `sudo apt-get install python3 python3-pip python3-venv`

### Erro ao ativar ambiente virtual no PowerShell

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro: "pip não encontrado"

**Windows:**
```powershell
python -m ensurepip --upgrade
```

**Linux/Mac:**
```bash
sudo apt-get install python3-pip  # Ubuntu/Debian
# ou
brew install python3              # macOS
```

### Erro ao instalar opencv-python

**Linux - Dependências do sistema:**
```bash
sudo apt-get update
sudo apt-get install libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
```

**macOS:**
```bash
brew install opencv
```

### Câmera não abre

1. Verificar se nenhum outro programa está usando a câmera
2. Tentar alterar o `camera_id` no código (0, 1, 2, etc.)
3. Verificar permissões da câmera (especialmente no macOS)

### Ambiente virtual não aparece no prompt

Isso é normal - o ambiente virtual pode estar ativo mesmo sem mostrar `(venv)`. 
Verificar com:
```bash
which python  # Linux/Mac
where python  # Windows
```
Deve apontar para `venv/Scripts/python` ou `venv/bin/python`

## Próximos Passos

Após instalação bem-sucedida:

1. Execute um dos detectores para testar
2. Consulte o README.md para detalhes sobre cada detector
3. Ajuste os parâmetros conforme necessário no código

## Desinstalação

Para remover o ambiente virtual:

```bash
# Desativar primeiro
deactivate

# Remover pasta (Windows)
rmdir /s venv

# Remover pasta (Linux/Mac)
rm -rf venv
```

## Comandos Rápidos

**Ativar ambiente virtual:**
- Windows: `venv\Scripts\Activate.ps1`
- Linux/Mac: `source venv/bin/activate`

**Desativar ambiente virtual:**
```bash
deactivate
```

**Reinstalar dependências:**
```bash
pip install --upgrade -r requirements.txt
```

**Verificar versões instaladas:**
```bash
pip list
```

## Suporte

Se encontrar problemas não listados aqui:
1. Verificar se todas as versões estão corretas
2. Consultar logs de erro completos
3. Verificar documentação do OpenCV: https://docs.opencv.org/

