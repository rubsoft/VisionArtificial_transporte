
#  vehicle_tracker.py v.01 - Ruben Monrroy Condori
#  Esta clase encapsula el algoritmo de Seguimiento Multi-Objeto (MOT). 


class VehicleTracker:
    def __init__(self, tracking_algorithm: str = "OC_SORT", max_age: int = 10):
        # Inicializa el tracker (e.g., OC-SORT, DeepSORT con Kalman Filter)
        # max_age define cuántos frames puede faltar una detección antes de descartar el tracklet [1]
        self.tracker = self._initialize_mot(tracking_algorithm)
        
    def update(self, detections: list, frame) -> list:
        # 1. Ejecuta la predicción (Kalman Filter) para tracklets existentes.
        # 2. Asocia las detecciones actuales con los tracklets existentes (Matching).
        # 3. Asigna nuevos IDs a detecciones no asociadas.
        # Retorna: Lista de Tracklets actualizados (BB, Class, track_id, Centroid)
        return updated_tracklets