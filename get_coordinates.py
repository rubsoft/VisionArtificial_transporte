# get_coordinates.py

import cv2
import config

# Variable global para almacenar los puntos
points = []

def click_event(event, x, y, flags, params):
    """
    Función callback que se ejecuta al hacer clic con el ratón.
    Guarda y dibuja las coordenadas del punto donde se hizo clic.
    """
    # Si el evento es un clic izquierdo
    if event == cv2.EVENT_LBUTTONDOWN:
        # Imprime las coordenadas en la consola
        print(f"Punto capturado: ({x}, {y})")
        
        # Almacena el punto
        points.append((x, y))
        
        # Dibuja un círculo en el punto donde se hizo clic
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        
        # Si ya hay más de un punto, dibuja una línea desde el anterior
        if len(points) > 1:
            cv2.line(img, points[-2], points[-1], (0, 255, 0), 2)
        
        cv2.imshow('Imagen - Haz clic en las esquinas de la ROI', img)

# --- Script Principal ---
# Cargar el video desde la configuración
cap = cv2.VideoCapture(config.VIDEO_PATH)
if not cap.isOpened():
    print("Error al abrir el video.")
    exit()

# Leer solo el primer fotograma
ret, img = cap.read()
if not ret:
    print("No se pudo leer el primer fotograma del video.")
    exit()

cap.release()

# Mostrar la imagen en una ventana
cv2.imshow('Imagen - Haz clic en las esquinas de la ROI', img)

# Establecer la función 'click_event' como el callback para eventos de ratón
cv2.setMouseCallback('Imagen - Haz clic en las esquinas de la ROI', click_event)

print("ℹ️  Haz clic en las esquinas de tu Zona de Interés (ROI) en orden.")
print("ℹ️  Cuando termines, presiona cualquier tecla para cerrar la ventana.")

# Esperar a que se presione una tecla
cv2.waitKey(0)

# Cerrar todas las ventanas
cv2.destroyAllWindows()

print("\n--- Puntos de la ROI capturados ---")
print("Copia el siguiente array de NumPy en tu archivo 'config.py'")
print(f"ROI_CORNERS = np.array({points}, np.int32)")