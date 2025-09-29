#  Violation_monitor.py v.01 - Ruben Monrroy Condori
#  Esta clase implementa la lógica central de la permanencia y el manejo temporal.

import cv2
import numpy as np

class ViolationMonitor:
    def __init__(self, fps: int, violation_time_min: int, roi_polygon: np.ndarray):
        self.fps = fps
        # Umbral de frames requerido para confirmar la infracción (ej. 5 min * 60 seg * 30 FPS)
        self.violation_frame_threshold = violation_time_min * 60 * fps
        self.discard_frame_threshold = 10  # Frames de tolerancia a oclusión [1]
        # Almacena el estado de cada vehículo tracked
        self.active_tracks = {} # {track_id: {'frames_present': N, 'last_seen_frame': T, 'is_infraction': False}}
        self.infractions =
        # Definición del polígono de la ROI (Región de Interés)
        self.roi = np.array(roi_polygon, dtype=np.int32) 

    def _is_inside_roi(self, centroid: tuple) -> bool:
        # Usa la función de OpenCV para verificar si el punto está dentro del polígono
        return cv2.pointPolygonTest(self.roi, centroid, False) > 0 

    def monitor_permanence(self, tracklets: list, current_frame_number: int):
        
        # 1. Actualizar estados de tracks observados en este frame
        current_ids = set()
        for track in tracklets:
            current_ids.add(track.id)
            centroid = track.centroid 

            if self._is_inside_roi(centroid):
                # Caso A: Vehículo presente en ROI
                if track.id not in self.active_tracks:
                    self.active_tracks[track.id] = {'frames_present': 1, 'last_seen_frame': current_frame_number, 'is_infraction': False}
                else:
                    self.active_tracks[track.id]['frames_present'] += 1
                    self.active_tracks[track.id]['last_seen_frame'] = current_frame_number

                # Verificar infracción
                if (not self.active_tracks[track.id]['is_infraction'] and 
                    self.active_tracks[track.id]['frames_present'] >= self.violation_frame_threshold):
                    self._trigger_alert(track.id, current_frame_number)
        
        # 2. Gestionar tracks ausentes (robustez a oclusión y descarte)
        for track_id in list(self.active_tracks.keys()):
            if track_id not in current_ids:
                # El vehículo no fue detectado en este frame, verificar si ha excedido el descarte
                frames_missing = current_frame_number - self.active_tracks[track_id]['last_seen_frame']
                if frames_missing > self.discard_frame_threshold:
                    # Si ha excedido el umbral, el tracklet debe ser descartado (o movido a caché de Re-ID)
                    del self.active_tracks[track_id]

    def _trigger_alert(self, track_id, current_frame_number):
        #... Lógica para generar evidencia y registro de la infracción...
        self.active_tracks[track_id]['is_infraction'] = True
        # (Ejemplo: Etiquetar con color rojo en la visualización [1])
        pass