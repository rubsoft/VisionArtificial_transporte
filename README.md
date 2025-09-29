### Clases Centrales del Sistema:

1.  **`DetectionProcessor` (Detección)**:
    *   **Responsabilidad:** Carga del modelo YOLO optimizado (TensorRT/PyTorch) y ejecución de inferencia en GPU.
    *   **Salida:** Lista de detecciones (`Bounding Boxes`, `Score`, `Clase`).

2.  **`VehicleTracker` (Seguimiento)**:
    *   **Responsabilidad:** Implementación del algoritmo MOT (OC-SORT/DeepSORT). Gestiona las predicciones de posición (Filtro de Kalman) y la asociación de detecciones a `track_id` únicos.
    *   **Salida:** Lista de `Tracklets` actualizados (`BB`, `track_id`, `Centroid`).

3.  **`ViolationMonitor` (Lógica de Permanencia)**:
    *   **Responsabilidad:** Módulo crítico para la validación de la infracción.
    *   **Funcionalidad Clave:**
        *   Define la **Región de Interés (ROI)** como un polígono geométrico.[3]
        *   Verifica la intersección del centroide del vehículo con la ROI (utilizando `cv2.pointPolygonTest` [3]).
        *   Gestiona el contador de `frames_presentes` para cada `track_id`.[1]
        *   Aplica un umbral de descarte temporal (e.g., 10 *frames*) para tolerar oclusiones breves y evitar el reinicio del temporizador.[1]
        *   Convierte el número de *frames* a tiempo real: $\text{Tiempo} = \text{Frames} / \text{FPS}$.
        *   Genera la alerta y el paquete de metadatos verificables cuando se excede el umbral de permanencia.

## 4. Requerimientos Técnicos y Despliegue (Edge AI)

Para lograr la operación en tiempo real (>30 FPS) requerida en vigilancia [4], el despliegue debe optimizarse en el borde (`Edge Computing`).

## 5. Instalación y Ejecución
# Instalación de dependencias de CV y Seguimiento
pip install opencv-python numpy
