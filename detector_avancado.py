"""
Detector avançado de pessoa usando OpenCV
Versão com mais opções de configuração e análise de posição
"""

import cv2
import numpy as np
from datetime import datetime

class DetectorPessoa:
    def __init__(self, camera_id=0, mostrar_fps=True):
        """
        Inicializa o detector de pessoa
        
        Args:
            camera_id: ID da câmera (0 = câmera padrão)
            mostrar_fps: Se True, mostra FPS na tela
        """
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise ValueError(f"Não foi possível abrir a câmera {camera_id}")
        
        # Configurações da câmera
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Inicializa detector HOG
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
        self.mostrar_fps = mostrar_fps
        self.fps = 0
        self.frame_count = 0
        self.tempo_inicio = cv2.getTickCount()
        
        # Histórico de detecções
        self.historico_deteccoes = []
        
    def calcular_fps(self):
        """Calcula e atualiza o FPS"""
        self.frame_count += 1
        tempo_atual = cv2.getTickCount()
        tempo_decorrido = (tempo_atual - self.tempo_inicio) / cv2.getTickFrequency()
        
        if tempo_decorrido > 1.0:  # Atualiza a cada segundo
            self.fps = self.frame_count / tempo_decorrido
            self.frame_count = 0
            self.tempo_inicio = tempo_atual
    
    def detectar_pessoas(self, frame, min_confidence=0.3):
        """
        Detecta pessoas no frame
        
        Args:
            frame: Frame de vídeo
            min_confidence: Confiança mínima para considerar detecção válida
        
        Returns:
            Lista de tuplas (x, y, w, h, confidence) para cada pessoa detectada
        """
        # Redimensiona para melhor performance
        frame_resized = cv2.resize(frame, (640, 480))
        
        # Detecta pessoas
        boxes, weights = self.hog.detectMultiScale(
            frame_resized,
            winStride=(8, 8),
            padding=(16, 16),
            scale=1.05,
            hitThreshold=min_confidence
        )
        
        # Filtra por confiança e ajusta coordenadas para o frame original
        scale_x = frame.shape[1] / 640
        scale_y = frame.shape[0] / 480
        
        deteccoes = []
        for (x, y, w, h), weight in zip(boxes, weights):
            if weight >= min_confidence:
                x_original = int(x * scale_x)
                y_original = int(y * scale_y)
                w_original = int(w * scale_x)
                h_original = int(h * scale_y)
                deteccoes.append((x_original, y_original, w_original, h_original, weight))
        
        return deteccoes
    
    def desenhar_deteccoes(self, frame, deteccoes):
        """
        Desenha retângulos e informações sobre as detecções
        
        Args:
            frame: Frame de vídeo
            deteccoes: Lista de detecções
        """
        altura_frame = frame.shape[0]
        largura_frame = frame.shape[1]
        
        # Desenha linha central (útil para câmera acima da cabeça)
        cv2.line(frame, (largura_frame // 2, 0), (largura_frame // 2, altura_frame), 
                (255, 255, 0), 1)
        cv2.line(frame, (0, altura_frame // 2), (largura_frame, altura_frame // 2), 
                (255, 255, 0), 1)
        
        for i, (x, y, w, h, confidence) in enumerate(deteccoes):
            # Cor baseada na confiança
            cor = (0, int(255 * confidence), int(255 * (1 - confidence)))
            
            # Retângulo principal
            cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 2)
            
            # Centro da pessoa
            centro_x = x + w // 2
            centro_y = y + h // 2
            cv2.circle(frame, (centro_x, centro_y), 5, (0, 0, 255), -1)
            
            # Label com informações
            label = f'Pessoa {i+1}: {confidence:.2f}'
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            
            # Fundo para o texto
            cv2.rectangle(frame, (x, y - label_size[1] - 10), 
                         (x + label_size[0], y), cor, -1)
            cv2.putText(frame, label, (x, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Informações de posição (útil para câmera acima)
            offset_x = centro_x - largura_frame // 2
            offset_y = centro_y - altura_frame // 2
            pos_text = f'X:{offset_x:+4d} Y:{offset_y:+4d}'
            cv2.putText(frame, pos_text, (x, y + h + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Informações gerais
        info_y = 30
        cv2.putText(frame, f'Pessoas detectadas: {len(deteccoes)}', 
                   (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if self.mostrar_fps:
            cv2.putText(frame, f'FPS: {self.fps:.1f}', 
                       (10, info_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                       (0, 255, 0), 2)
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, timestamp, (largura_frame - 100, altura_frame - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def executar(self):
        """Loop principal de detecção"""
        print("Detector avançado iniciado!")
        print("Controles:")
        print("  'q' - Sair")
        print("  's' - Salvar screenshot")
        print("  'r' - Resetar estatísticas")
        
        screenshot_count = 0
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Erro: Não foi possível ler o frame")
                    break
                
                # Detecta pessoas
                deteccoes = self.detectar_pessoas(frame, min_confidence=0.3)
                
                # Atualiza histórico
                self.historico_deteccoes.append({
                    'timestamp': datetime.now(),
                    'count': len(deteccoes)
                })
                
                # Desenha detecções
                self.desenhar_deteccoes(frame, deteccoes)
                
                # Calcula FPS
                self.calcular_fps()
                
                # Mostra frame
                cv2.imshow('Detector de Pessoas - Avançado', frame)
                
                # Processa teclas
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    screenshot_count += 1
                    filename = f'screenshot_{screenshot_count:04d}.jpg'
                    cv2.imwrite(filename, frame)
                    print(f"Screenshot salvo: {filename}")
                elif key == ord('r'):
                    self.historico_deteccoes = []
                    self.frame_count = 0
                    self.tempo_inicio = cv2.getTickCount()
                    print("Estatísticas resetadas")
        
        except KeyboardInterrupt:
            print("\nInterrompido pelo usuário")
        
        finally:
            self.encerrar()
    
    def encerrar(self):
        """Libera recursos e encerra o detector"""
        self.cap.release()
        cv2.destroyAllWindows()
        
        # Estatísticas finais
        if self.historico_deteccoes:
            total_deteccoes = sum(h['count'] for h in self.historico_deteccoes)
            media_deteccoes = total_deteccoes / len(self.historico_deteccoes)
            print(f"\nEstatísticas:")
            print(f"  Total de frames processados: {len(self.historico_deteccoes)}")
            print(f"  Média de pessoas por frame: {media_deteccoes:.2f}")
        
        print("Detector encerrado!")


def main():
    try:
        detector = DetectorPessoa(camera_id=0, mostrar_fps=True)
        detector.executar()
    except Exception as e:
        print(f"Erro: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())

