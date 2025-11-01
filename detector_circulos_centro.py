"""
Detector de círculos no centro da imagem
Especializado para medir diâmetro de cabeça (visão superior)
"""

import cv2
import numpy as np
from datetime import datetime

class DetectorCirculoCentro:
    def __init__(self, camera_id=0):
        """Inicializa o detector"""
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise ValueError(f"Não foi possível abrir a câmera {camera_id}")
        
        # Configurações da câmera
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Parâmetros de detecção
        self.param1 = 50
        self.param2 = 30
        self.min_radius_percent = 0.10  # 10% = diâmetro 20%
        self.max_radius_percent = 0.25  # 25% = diâmetro 50%
        
        # Área central para detecção (60% do centro)
        self.zona_centro_percent = 0.60
        
        # Fator de calibração (pixels para cm)
        # Estimativa inicial: assumindo cabeça média ~18cm a ~60cm de distância
        # Será ajustado automaticamente ou pode ser calibrado
        self.calibracao_px_cm = None
        
        # Estado
        self.diametro_detectado = None
        self.medicao_realizada = False
        
    def calcular_fator_calibracao(self, raio_pixels, largura_imagem):
        """
        Calcula fator de calibração baseado em estimativas
        Assumindo que uma cabeça humana média tem ~16-20cm de diâmetro
        e que o diâmetro detectável corresponde a essa faixa
        """
        # Se ainda não calibrado, usa estimativa inicial
        if self.calibracao_px_cm is None:
            # Estimativa: diâmetro médio de cabeça = 18cm
            # Se o círculo ocupa entre 20-50% da imagem, estimamos
            # que está a uma distância que faz com que isso corresponda
            # a uma cabeça de tamanho médio
            diâmetro_medio_cm = 18.0
            diâmetro_pixels = raio_pixels * 2
            
            # Fator aproximado baseado na proporção esperada
            # Cabeça ocupa aproximadamente 20-40% da largura quando detectável
            # Vamos usar uma estimativa baseada no raio detectado
            self.calibracao_px_cm = diâmetro_pixels / diâmetro_medio_cm
        
        return self.calibracao_px_cm
    
    def esta_na_zona_central(self, x, y, largura, altura):
        """Verifica se o círculo está na zona central"""
        centro_x = largura // 2
        centro_y = altura // 2
        zona_largura = largura * self.zona_centro_percent
        zona_altura = altura * self.zona_centro_percent
        
        return (abs(x - centro_x) < zona_largura / 2 and 
                abs(y - centro_y) < zona_altura / 2)
    
    def esta_pronto_para_medir(self, circulo_central, min_radius, max_radius, largura, altura):
        """Verifica se o círculo está pronto para medir (dentro da área e tamanho válido)"""
        if circulo_central is None:
            return False
        
        x, y, r = circulo_central
        
        # Verifica se está na zona central
        if not self.esta_na_zona_central(x, y, largura, altura):
            return False
        
        # Verifica se o raio está dentro dos limites permitidos
        if r < min_radius or r > max_radius:
            return False
        
        return True
    
    def detectar_circulo_central(self, frame):
        """Detecta círculos apenas na zona central"""
        altura, largura = frame.shape[:2]
        
        # Calcula limites de raio (20-50% do diâmetro = 10-25% do raio)
        min_radius = int(min(largura, altura) * self.min_radius_percent)
        max_radius = int(min(largura, altura) * self.max_radius_percent)
        
        # Converte para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Aplica desfoque gaussiano
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # Detecta círculos
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=min_radius * 2,
            param1=self.param1,
            param2=self.param2,
            minRadius=min_radius,
            maxRadius=max_radius
        )
        
        # Filtra apenas círculos na zona central
        circulo_central = None
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            
            for (x, y, r) in circles:
                if self.esta_na_zona_central(x, y, largura, altura):
                    circulo_central = (x, y, r)
                    break  # Pega o primeiro círculo central encontrado
        
        return circulo_central, min_radius, max_radius
    
    def desenhar_interface(self, frame, circulo_central, min_radius, max_radius, pronto_para_medir):
        """Desenha interface com orientações e marcações"""
        altura, largura = frame.shape[:2]
        centro_x = largura // 2
        centro_y = altura // 2
        
        # Calcula limites da zona central
        zona_largura = int(largura * self.zona_centro_percent)
        zona_altura = int(altura * self.zona_centro_percent)
        
        # Desenha retângulo da zona central (verde claro)
        x1 = centro_x - zona_largura // 2
        y1 = centro_y - zona_altura // 2
        x2 = centro_x + zona_largura // 2
        y2 = centro_y + zona_altura // 2
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        
        # Desenha círculos indicando limites de tamanho detectável
        # Círculo mínimo (20% diâmetro)
        cv2.circle(frame, (centro_x, centro_y), min_radius, (255, 0, 255), 1, cv2.LINE_AA)
        # Círculo máximo (50% diâmetro)
        cv2.circle(frame, (centro_x, centro_y), max_radius, (255, 0, 255), 1, cv2.LINE_AA)
        
        # Linhas centrais de referência
        cv2.line(frame, (centro_x, 0), (centro_x, altura), (255, 255, 0), 1)
        cv2.line(frame, (0, centro_y), (largura, centro_y), (255, 255, 0), 1)
        cv2.circle(frame, (centro_x, centro_y), 3, (255, 255, 0), -1)
        
        # Só desenha o círculo se estiver pronto para medir
        if circulo_central and pronto_para_medir:
            x, y, r = circulo_central
            # Círculo detectado (verde)
            cv2.circle(frame, (x, y), r, (0, 255, 0), 3)
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
            
            # Linha do centro até o círculo
            cv2.line(frame, (centro_x, centro_y), (x, y), (0, 255, 255), 2)
            
            # Calcula diâmetro em pixels
            diametro_px = r * 2
            
            # Se medição foi realizada, mostra resultado
            if self.medicao_realizada and self.diametro_detectado is not None:
                # Área destacada para resultado
                cv2.rectangle(frame, (10, altura - 120), (largura - 10, altura - 10), 
                             (0, 0, 0), -1)
                cv2.rectangle(frame, (10, altura - 120), (largura - 10, altura - 10), 
                             (0, 255, 0), 3)
                
                resultado_texto = f"Diametro detectado = {self.diametro_detectado:.2f} cm"
                texto_size = cv2.getTextSize(resultado_texto, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
                texto_x = (largura - texto_size[0]) // 2
                cv2.putText(frame, resultado_texto, (texto_x, altura - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            else:
                # Mostra informações do círculo detectado
                info_text = f"Raio: {r}px | Diametro: {diametro_px}px"
                cv2.putText(frame, info_text, (x - 80, y - r - 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Orientações para o usuário
        orientacoes = [
            "POSICIONE A CABECA NO CENTRO DA AREA AMARELA",
            f"Tamanho detectavel: {int(self.min_radius_percent*200)}% a {int(self.max_radius_percent*200)}% da imagem",
            "Pressione 'M' para MEDIR o diametro",
            "Pressione 'Q' para sair",
            "Pressione '+/-' para ajustar sensibilidade"
        ]
        
        y_offset = 30
        for i, texto in enumerate(orientacoes):
            # Fundo preto semi-transparente
            (w, h), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (10, y_offset - 20), (w + 20, y_offset + 10), 
                         (0, 0, 0), -1)
            cv2.putText(frame, texto, (15, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_offset += 35
        
        # Status de detecção
        if pronto_para_medir:
            status = "CIRCULO DETECTADO - Pronto para medir!"
            cor_status = (0, 255, 0)
        elif circulo_central:
            status = "Circulo detectado mas fora da area ou tamanho invalido"
            cor_status = (0, 165, 255)
        else:
            status = "Aguardando circulo no centro..."
            cor_status = (0, 165, 255)
        
        cv2.putText(frame, status, (10, altura - 140),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_status, 2)
    
    def realizar_medicao(self, circulo_central, largura_imagem):
        """Realiza a medição do diâmetro"""
        if circulo_central is None:
            return False
        
        x, y, r = circulo_central
        diametro_px = r * 2
        
        # Calcula fator de calibração se necessário
        if self.calibracao_px_cm is None:
            self.calcular_fator_calibracao(r, largura_imagem)
        
        # Converte para cm
        diametro_cm = diametro_px / self.calibracao_px_cm
        
        self.diametro_detectado = diametro_cm
        self.medicao_realizada = True
        
        return True
    
    def executar(self):
        """Loop principal"""
        print("=" * 50)
        print("Detector de Circulo no Centro")
        print("=" * 50)
        print("\nOrientacoes:")
        print("  1. Posicione a cabeca no centro da area amarela")
        print("  2. O tamanho detectavel e de 20% a 50% da imagem")
        print("  3. Pressione 'M' para medir o diametro")
        print("  4. Pressione '+/-' para ajustar sensibilidade")
        print("  5. Pressione 'Q' para sair")
        print("=" * 50)
        
        frame_count = 0
        tempo_inicio = cv2.getTickCount()
        fps = 0
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Erro: Não foi possível ler o frame")
                    break
                
                frame_count += 1
                
                # Detecta círculo central
                circulo_central, min_radius, max_radius = self.detectar_circulo_central(frame)
                
                # Verifica se está pronto para medir
                altura, largura = frame.shape[:2]
                pronto_para_medir = self.esta_pronto_para_medir(circulo_central, min_radius, max_radius, largura, altura)
                
                # Desenha interface
                self.desenhar_interface(frame, circulo_central, min_radius, max_radius, pronto_para_medir)
                
                # Calcula FPS
                tempo_atual = cv2.getTickCount()
                tempo_decorrido = (tempo_atual - tempo_inicio) / cv2.getTickFrequency()
                if tempo_decorrido > 1.0:
                    fps = frame_count / tempo_decorrido
                    frame_count = 0
                    tempo_inicio = tempo_atual
                
                # Mostra FPS
                altura = frame.shape[0]
                cv2.putText(frame, f'FPS: {fps:.1f}', (frame.shape[1] - 120, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Mostra frame
                cv2.imshow('Detector de Circulo - Centro', frame)
                
                # Processa teclas
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('m') or key == ord('M'):
                    largura = frame.shape[1]
                    if pronto_para_medir:
                        if self.realizar_medicao(circulo_central, largura):
                            print(f"\n>>> MEDICAO REALIZADA: Diametro = {self.diametro_detectado:.2f} cm <<<")
                    elif circulo_central:
                        print("ERRO: Circulo detectado mas nao esta pronto para medir (fora da area ou tamanho invalido).")
                    else:
                        print("ERRO: Nenhum circulo detectado no centro. Posicione a cabeca corretamente.")
                elif key == ord('+') or key == ord('='):
                    self.param2 = max(self.param2 - 5, 10)
                    print(f"Sensibilidade aumentada. Param2: {self.param2}")
                elif key == ord('-') or key == ord('_'):
                    self.param2 = min(self.param2 + 5, 100)
                    print(f"Sensibilidade diminuida. Param2: {self.param2}")
                elif key == ord('r') or key == ord('R'):
                    self.medicao_realizada = False
                    self.diametro_detectado = None
                    self.calibracao_px_cm = None
                    print("Medicao resetada")
        
        except KeyboardInterrupt:
            print("\nInterrompido pelo usuario")
        
        finally:
            self.encerrar()
    
    def encerrar(self):
        """Libera recursos"""
        self.cap.release()
        cv2.destroyAllWindows()
        
        if self.medicao_realizada:
            print(f"\nMedicao final: {self.diametro_detectado:.2f} cm")
        
        print("Detector encerrado!")


def main():
    try:
        detector = DetectorCirculoCentro(camera_id=0)
        detector.executar()
    except Exception as e:
        print(f"Erro: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())

