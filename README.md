subgraph Módulos
    B;
    C;
    D;
end

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

### 4.1. Hardware Recomendado

*   **Plataforma:** **NVIDIA Jetson Orin NX o AGX Orin**.
*   **Justificación:** La arquitectura Orin ofrece un rendimiento significativamente superior (2x a 3x de aceleración en modo MAX-N) para tareas de inferencia de *Deep Learning* comparado con generaciones anteriores (Xavier).[5, 6]
*   **Memoria:** Mínimo de 8 GB de RAM unificada.

### 4.2. Optimización de Software

*   **NVIDIA TensorRT:** Obligatorio. Permite la optimización del modelo (fusión de capas, cuantificación a FP16/INT8), resultando en una aceleración de 2x a 3x en la velocidad de inferencia respecto a la ejecución nativa (PyTorch/ONNX).[6]

## 5. Entrenamiento y Preparación del Dataset

El rigor académico requiere un *dataset* local bien curado y una estrategia de *fine-tuning* eficiente.

### 5.1. Dataset y Anotación

*   **Herramientas:** Se recomienda el uso de herramientas como **CVAT** o **Label Studio** para la generación de anotaciones precisas en formato YOLO (`bounding boxes`).[7]
*   **Estrategia Avanzada:** Para reducir el esfuerzo de anotación manual, se puede implementar la generación de **pseudo anotaciones** utilizando un modelo pre-entrenado (como SAM o Box2Mask) ajustado con un pequeño conjunto de datos manualmente etiquetado.[8]

### 5.2. Aumento de Datos (Data Augmentation)

Para garantizar la robustez ante la variabilidad del entorno urbano (24/7), el *Data Augmentation* es fundamental para mitigar el *overfitting* [9]:

*   **Geométricas:** Rotación, traslación, volteo horizontal (`Flip`).[10]
*   **Color/Brillo:** Variación de contraste, ajuste de brillo, valor de gris (`Grayscale`).[10]
*   **Avanzadas:** **Mosaic** y **CutMix**, para mejorar la detección de objetos pequeños en escenas congestionadas.[9, 10]

## 6. Métricas de Evaluación Clave

La validación del sistema no solo debe centrarse en la detección (mAP), sino especialmente en la calidad del seguimiento:

| Métrica | Definición | Requisito Académico |
| :--- | :--- | :--- |
| **IDF1 Score** (Identity F1) | Mide la precisión en el mantenimiento de la identidad correcta (`track_id`) a lo largo del tiempo. | **Métrica principal** para este proyecto. Un alto IDF1 (> 70%) asegura que el temporizador de permanencia es exacto. |
| **ID Switch Rate (ISR)** | Tasa de errores en la asignación de identidad. | Debe ser minimizado (Ideal < 2%). Altos ISR invalidan las alertas de permanencia. |
| **FPS** (Frames per Second) | Tasa de procesamiento del sistema completo (Detección + Tracking + Lógica). | Operación en tiempo real (> 30 FPS).[4] |

## 7. Instalación y Ejecución

### 7.1. Dependencias (Ejemplo)

```bash
# Entorno de Python recomendado
conda create -n vision_permanencia python=3.10
conda activate vision_permanencia

# Instalación de PyTorch (con soporte CUDA)
# (Asegurar la versión compatible con la Jetson o el entorno de desarrollo)
# pip install torch torchvision torchaudio

# Instalación de Ultralytics (YOLOv8/v9)
pip install ultralytics

# Instalación de dependencias de CV y Seguimiento (ej. OC-SORT/DeepSORT)
pip install opencv-python numpy
# git clone [https://github.com/mikel-brostrom/yolo_tracking.git](https://github.com/mikel-brostrom/yolo_tracking.git) # Ejemplo para tracking