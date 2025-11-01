# Quick Start - Início Rápido

Guia rápido para começar a usar o projeto em 5 minutos.

## Pré-requisitos

- Python 3.7+ instalado
- Git (ou baixar ZIP do repositório)

## Instalação Rápida (3 comandos)

### Windows (PowerShell)

```powershell
# 1. Clonar/Baixar projeto
git clone <URL_DO_REPO>
cd athena-js

# 2. Setup automático
setup.bat

# 3. Executar (após setup)
venv\Scripts\Activate.ps1
python detector_circulos_centro.py
```

### Linux/Mac

```bash
# 1. Clonar/Baixar projeto
git clone <URL_DO_REPO>
cd athena-js

# 2. Setup automático
python3 setup.py

# 3. Executar (após setup)
source venv/bin/activate
python3 detector_circulos_centro.py
```

## Comandos Essenciais

**Ativar ambiente virtual:**
- Windows: `venv\Scripts\Activate.ps1`
- Linux/Mac: `source venv/bin/activate`

**Executar detectores:**
```bash
python detector_circulos_centro.py  # Recomendado
python detector_basico.py
python detector_avancado.py
```

**Desativar ambiente virtual:**
```bash
deactivate
```

## Problemas?

Consulte [INSTALACAO.md](INSTALACAO.md) para guia completo e solução de problemas.

