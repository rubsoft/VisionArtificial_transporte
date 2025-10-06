# config.py
import numpy as np

# --- Rutas y Modelos ---
VIDEO_PATH = 'data/test_video.mp4'
# VIDEO_PATH = "rtsp://usuario:contraseña@192.168.1.100/stream1"

MODEL_PATH = 'yolov8n.pt'  # Usamos el nano por velocidad, puedes cambiarlo a 'yolov8s.pt'
EVIDENCE_DIR = 'evidences/' # Directorio para guardar las pruebas de infracción

# --- Parámetros de Detección y Seguimiento ---
VEHICLE_CLASSES = [2, 3, 5, 7]  # COCO IDs for car, motorcycle, bus, truck
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.4 # Umbral de superposición para el tracker

# --- Lógica de Infracción ---
# Coordenadas de la Zona de Interés (ROI). Ajusta estos valores a tu video.

ROI_CORNERS = np.array([(431, 305), (555, 282), (575, 267), (594, 259), (681, 294), (620, 328), (534, 359), (502, 378), (480, 384), (432, 308), (432, 308)], np.int32)

#ROI_CORNERS = np.array([
#    [50, 200], [1200, 200], [1200, 700], [50, 700]
#], np.int32)

# Tiempo máximo de permanencia permitido en segundos
MAX_PERMANENCE_SECONDS = 10 
# Adecuar 