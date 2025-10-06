# main.py
import cv2
import os
import time
import numpy as np
from ultralytics import YOLO
import config
from utils.tracker import IoUTracker

class InfractionSystem:
    def __init__(self):
        # 1. Cargar todos los recursos en el constructor
        self.model = YOLO(config.MODEL_PATH)
        self.tracker = IoUTracker()
        self.cap = cv2.VideoCapture(config.VIDEO_PATH)
        if not self.cap.isOpened():
            raise IOError(f"No se pudo abrir el video en '{config.VIDEO_PATH}'")
        
        # 2. El estado del sistema ahora es un atributo de la clase
        self.tracked_vehicles = {}
        
        # Crear directorio de evidencias
        os.makedirs(config.EVIDENCE_DIR, exist_ok=True)
        print("Sistema de Infracciones inicializado.")

    def _record_infraction(self, frame, vehicle_id, box):
        """guardar la evidencia."""
        x1, y1, x2, y2 = box
        vehicle_image = frame[max(0, y1):min(frame.shape[0], y2), max(0, x1):min(frame.shape[1], x2)]
        ## no funciona ... remodelar 10 segunds
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(config.EVIDENCE_DIR, f"infraction_id_{vehicle_id}_{timestamp}.jpg")
        cv2.imwrite(filename, vehicle_image) ## seria bueno hasta identificar la placa y enviar el gps
        print(f"🚨 ¡Infracción registrada! Evidencia para ID {vehicle_id} guardada.")

    def process_frame(self, frame):
        """Procesa un solo fotograma para detectar y rastrear vehículos."""
        # Detección de vehículos
        results = self.model(frame, classes=config.VEHICLE_CLASSES, conf=config.CONFIDENCE_THRESHOLD, verbose=False)
        detections = []
        for result in results[0].boxes.data.cpu().numpy():
            x1, y1, x2, y2, _, _ = result
            detections.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])
        
        # Seguimiento de vehículos
        tracked_objects = self.tracker.update(detections)
        
        current_time = time.time()
        
        # Lógica de permanencia y alerta
        for obj in tracked_objects:
            x, y, w, h, obj_id = obj
            x1, y1, x2, y2 = x, y, x + w, y + h
            center_point = (int(x + w / 2), int(y + h / 2))
            
            #esta en el vehiculo en el area..
            is_inside = cv2.pointPolygonTest(config.ROI_CORNERS, center_point, False) >= 0
            
            if is_inside:
                if obj_id not in self.tracked_vehicles:
                    self.tracked_vehicles[obj_id] = {"entry_time": current_time, "infraction_recorded": False}
                
                permanence_time = current_time - self.tracked_vehicles[obj_id]["entry_time"]
                
                color = (0, 255, 255) # Amarillo
                if permanence_time > config.MAX_PERMANENCE_SECONDS:
                    color = (0, 0, 255) # Rojo
                    if not self.tracked_vehicles[obj_id]["infraction_recorded"]:
                        self._record_infraction(frame, obj_id, (x1, y1, x2, y2))
                        self.tracked_vehicles[obj_id]["infraction_recorded"] = True
                
                # Visualización
                label = f"ID: {obj_id} | {int(permanence_time)}s"
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            else:
                if obj_id in self.tracked_vehicles:
                    del self.tracked_vehicles[obj_id]
        return frame

    def run(self):
        """Bucle principal para procesar el video."""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Fin del video.")
                break
            
            # Dibujar la ROI
            cv2.polylines(frame, [config.ROI_CORNERS], isClosed=True, color=(255, 0, 0), thickness=2)
            
            # Procesar el fotograma
            processed_frame = self.process_frame(frame)
            
            # Mostrar resultado
            cv2.imshow("Sistema de Detección de Infracciones", processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Limpieza
        self.cap.release()
        cv2.destroyAllWindows()
        print("Sistema detenido.")

if __name__ == "__main__":
    try:
        system = InfractionSystem()
        system.run()
    except Exception as e:
        print(f"Ocurrió un error: {e}")