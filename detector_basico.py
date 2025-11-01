"""
Detector básico de pessoa usando OpenCV
Captura vídeo da câmera do notebook e detecta pessoas usando HOG
"""

import cv2

def main():
    # Inicializa a captura de vídeo (0 = câmera padrão do notebook)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera")
        return
    
    # Inicializa o detector HOG (Histogram of Oriented Gradients) para pessoas
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    print("Detector iniciado! Pressione 'q' para sair")
    
    while True:
        # Captura frame por frame
        ret, frame = cap.read()
        
        if not ret:
            print("Erro: Não foi possível ler o frame")
            break
        
        # Redimensiona o frame para melhor performance (opcional)
        frame_resized = cv2.resize(frame, (640, 480))
        
        # Detecta pessoas no frame
        boxes, weights = hog.detectMultiScale(
            frame_resized,
            winStride=(8, 8),
            padding=(16, 16),
            scale=1.05,
            hitThreshold=0.5
        )
        
        # Desenha retângulos ao redor das pessoas detectadas
        for (x, y, w, h), weight in zip(boxes, weights):
            cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame_resized,
                f'Pessoa {weight:.2f}',
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
        
        # Adiciona texto informativo
        cv2.putText(
            frame_resized,
            f'Pessoas detectadas: {len(boxes)}',
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
        # Mostra o frame
        cv2.imshow('Detector de Pessoas', frame_resized)
        
        # Sai do loop quando 'q' é pressionado
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Libera a captura e fecha as janelas
    cap.release()
    cv2.destroyAllWindows()
    print("Detector encerrado!")

if __name__ == "__main__":
    main()

