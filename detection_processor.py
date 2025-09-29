
#  detection_processor.py  v0 - Ruben Monrroy Condori
#  Esta clase es responsable de cargar y ejecutar el modelo CNN optimizado (YOLOv8x/v9).
#  La eficiencia requiere que la carga sea un motor TensorRT precompilado.



class DetectionProcessor:
    def __init__(self, model_path: str, device: str = 'cuda'):
        # Carga el modelo YOLO optimizado (PyTorch o TensorRT engine)
        self.model = self._load_model(model_path, device)
        
    def detect(self, frame) -> list:
        # Pre-procesa el frame (escalado, normalización)
        # Ejecuta la inferencia en el dispositivo (GPU)
        # Filtra por score de confianza (ej. > 0.3)
        # Retorna: Lista de Detecciones (BB: [x1, y1, x2, y2], Score, Clase)
        return detections