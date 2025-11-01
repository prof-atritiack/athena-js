# Detector de Pessoas com OpenCV

Sistema de detecção de pessoas usando OpenCV e Python, desenvolvido para funcionar com uma câmera posicionada acima da cabeça de uma pessoa.

## Requisitos

- Python 3.7 ou superior
- Webcam conectada ao notebook/computador

## Instalação

> **Início Rápido:** Para começar em 5 minutos, veja [QUICKSTART.md](QUICKSTART.md)  
> **Guia Completo:** Para instruções detalhadas passo a passo, consulte [INSTALACAO.md](INSTALACAO.md)

### Opção 1: Setup Automático (Recomendado)

**Windows:**
```bash
setup.bat
```

**Linux/Mac ou Cross-platform:**
```bash
python setup.py
# ou
python3 setup.py
```

### Opção 2: Setup Manual

#### 1. Criar ambiente virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

#### 2. Instalar dependências

Com o ambiente virtual ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

### Ativar ambiente virtual (já criado)

**Windows:**
- Execute `ativar_ambiente.bat`, ou
- No PowerShell: `venv\Scripts\Activate.ps1`, ou
- No CMD: `venv\Scripts\activate.bat`

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Desativar ambiente virtual

Quando terminar de trabalhar, você pode desativar o ambiente virtual com:
```bash
deactivate
```

## Uso

### Detector de Círculos no Centro (Especializado - Medição de Diâmetro)

Execute o detector especializado para medir diâmetro de cabeça no centro da imagem:

```bash
python detector_circulos_centro.py
```

**Controles:**
- `m` ou `M` - **Medir** o diâmetro detectado
- `q` ou `Q` - Sair do programa
- `+` ou `=` - Aumentar sensibilidade
- `-` ou `_` - Diminuir sensibilidade
- `r` ou `R` - Resetar medição

**Recursos:**
- Detecta círculos **apenas no centro** da imagem (60% da área central)
- Diâmetro detectável: **20% a 50%** da medida da imagem
- Área detectável marcada com círculos guia (roxa)
- Zona central marcada (amarelo)
- **Medição de diâmetro em cm** ao pressionar 'M'
- Orientações visuais na tela
- Calibração automática baseada em tamanho médio de cabeça

**Como usar:**
1. Posicione a cabeça no centro da área amarela
2. Aguarde o círculo verde aparecer (detecção confirmada)
3. Pressione **'M'** para medir
4. Veja o resultado: **"Diametro detectado = ___ cm"**

### Detector Básico (Pessoas completas)

Execute o detector básico para detectar pessoas inteiras:

```bash
python detector_basico.py
```

**Controles:**
- `q` - Sair do programa

### Detector Avançado (Pessoas completas)

Execute o detector avançado com mais recursos:

```bash
python detector_avancado.py
```

**Controles:**
- `q` - Sair do programa
- `s` - Salvar screenshot do frame atual
- `r` - Resetar estatísticas

**Recursos do detector avançado:**
- Exibição de FPS em tempo real
- Linhas de referência central (úteis para câmera acima)
- Informações de posição (offset X e Y do centro)
- Níveis de confiança por detecção
- Timestamp no vídeo
- Estatísticas ao encerrar

## Como Funciona

### Detector de Círculos

O detector de círculos utiliza a **Transformada de Hough para círculos** do OpenCV, que é ideal para detectar objetos circulares. É especialmente útil quando a câmera está posicionada acima da cabeça, pois a cabeça vista de cima aparece como um círculo.

**Parâmetros principais:**
- `param1`: Limiar superior para detecção de bordas (Canny)
- `param2`: Limiar de acumulação - quanto menor, mais círculos detectados
- `minRadius` / `maxRadius`: Faixa de raio dos círculos a detectar

### Detectores de Pessoas

Os scripts utilizam o detector **HOG (Histogram of Oriented Gradients)** do OpenCV, que é eficiente para detecção de pedestres/pessoas em tempo real.

### Parâmetros Ajustáveis

No código, você pode ajustar:

- `winStride`: Passo da janela deslizante (padrão: 8x8)
- `padding`: Padding ao redor das detecções (padrão: 16x16)
- `scale`: Fator de escala para detecção multi-escala (padrão: 1.05)
- `hitThreshold`: Confiança mínima (padrão: 0.5)
- `min_confidence`: Filtro adicional de confiança (padrão: 0.3)

## Exemplos de Uso

### Para câmera acima da cabeça:

**Detector de Círculos** - É o mais recomendado para este cenário:
- Detecta a cabeça como um círculo (visão de cima)
- Mostra offset preciso da posição da cabeça
- Permite ajuste de sensibilidade em tempo real
- Ideal para rastreamento de posição

**Detector Avançado** - Alternativa com HOG:
- Mostra linhas de referência central
- Informações de offset X e Y do centro da pessoa
- Útil se você precisar detectar o corpo inteiro

## Troubleshooting

### Câmera não abre

- Verifique se a câmera não está sendo usada por outro programa
- Tente alterar o `camera_id` no código (0, 1, 2, etc.)

### Performance baixa

- Reduza a resolução do vídeo no código
- Aumente o `winStride` para reduzir processamento
- Ajuste o `scale` para fazer menos escalas

### Muitas detecções falsas

- Aumente o `min_confidence` ou `hitThreshold`
- Melhore a iluminação do ambiente
- Ajuste os parâmetros de detecção

## Próximos Passos

- [ ] Adicionar detecção usando YOLO para maior precisão
- [ ] Implementar rastreamento de pessoas entre frames
- [ ] Adicionar salvamento de vídeo com detecções
- [ ] Calibração para câmera fixa acima da cabeça
- [ ] Análise de movimento e direção

## Notas

Estes scripts são exemplos básicos para começar. Para produção, considere:
- Usar YOLO ou modelos mais modernos
- Implementar filtro de Kalman para rastreamento
- Calibrar a câmera para medidas precisas
- Otimizar para o hardware específico

## Referências

### Bibliotecas e Ferramentas

- **OpenCV**: Biblioteca de visão computacional utilizada para detecção e processamento de imagens
  - Documentação: https://opencv.org/
  - GitHub: https://github.com/opencv/opencv
  - Transformada de Hough para círculos: cv2.HoughCircles
  - Detector HOG para pessoas: cv2.HOGDescriptor

- **Python**: Linguagem de programação utilizada
  - Versão: Python 3.7 ou superior
  - Site oficial: https://www.python.org/

- **NumPy**: Biblioteca para cálculos numéricos
  - Utilizada para operações com arrays e manipulação de dados de imagem

### Desenvolvimento

Este projeto foi desenvolvido com auxílio de:

- **Cursor AI**: Editor de código com suporte a inteligência artificial
  - Website: https://cursor.sh/
  - Utilizado para desenvolvimento, geração de código e assistência durante a implementação

- **Modelo de IA**: Claude (Anthropic)
  - Utilizado através do Cursor AI para assistência no desenvolvimento
  - Referência: https://www.anthropic.com/

### Algoritmos Utilizados

- **Histogram of Oriented Gradients (HOG)**: Método para detecção de objetos, especialmente eficiente para detecção de pedestres
  - Dalal, N., & Triggs, B. (2005). Histograms of oriented gradients for human detection. CVPR.

- **Transformada de Hough para Círculos**: Método para detecção de formas circulares em imagens
  - Duda, R. O., & Hart, P. E. (1972). Use of the Hough transformation to detect lines and curves in pictures. Communications of the ACM.

### Licença

Este projeto é fornecido como está, sem garantias. Sinta-se livre para usar e modificar conforme necessário.

