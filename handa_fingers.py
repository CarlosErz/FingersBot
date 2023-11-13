import cv2
import mediapipe as mp
#---------------------------------------------
import serial
import time
#---------------------------------------------
import math

# ---------------------------------------------
# Configuración de OpenCV y MediaPipe
# ---------------------------------------------
mp_dibujo = mp.solutions.drawing_utils
mp_manos = mp.solutions.hands
cap = cv2.VideoCapture(0)

# ---------------------------------------------
# Configuración de la comunicación con Arduino
# ---------------------------------------------
# arduino = serial.Serial('COM4', 9600)

# ---------------------------------------------
# Bucle principal
# ---------------------------------------------



#funciones 
#---------------------------------------------

def calcular_distancia(punto_dedo, landmark_wrist):
                    return math.sqrt(
                        (punto_dedo.x - landmark_wrist.x) ** 2 +
                        (punto_dedo.y - landmark_wrist.y) ** 2 +
                        (punto_dedo.z - landmark_wrist.z) ** 2
                    )
                    
def redondear_distancia(distancia):
                    return round(distancia, 1) if distancia > 0.19 else 0.19
                    
def dibujar_rectangulo_y_texto(frame, punto_dedo, color_rectangulo=(0, 255, 0), color_texto=(255, 255, 255)):
    x, y = int(punto_dedo.x * frame.shape[1]), int(punto_dedo.y * frame.shape[0])
    cv2.rectangle(frame, (x - 10, y - 10), (x + 10, y + 10), color_rectangulo, 2)
    distancia_dedo = calcular_distancia(punto_dedo, landmarks.landmark[mp_manos.HandLandmark.WRIST])
    distancia_dedo = redondear_distancia(distancia_dedo)
    cv2.putText(frame, f"{distancia_dedo}", (x - 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_texto, 2)
    
#---------------------------------------------
                      
with mp_manos.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as manos:
    prev_puntas_dedos = [None, None, None, None, None]
    last_send_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = manos.process(frame_rgb)
        
        cv2.putText(frame, f"@Eanz", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        

        if resultados.multi_hand_landmarks:
            for landmarks in resultados.multi_hand_landmarks:
                puntas_dedos = [
                    landmarks.landmark[mp_manos.HandLandmark.THUMB_TIP],
                    landmarks.landmark[mp_manos.HandLandmark.INDEX_FINGER_TIP],
                    landmarks.landmark[mp_manos.HandLandmark.MIDDLE_FINGER_TIP],
                    landmarks.landmark[mp_manos.HandLandmark.RING_FINGER_TIP],
                    landmarks.landmark[mp_manos.HandLandmark.PINKY_TIP]
                ]

                umbral_cierre = 0.19

             
                    
            for i, punto_dedo in enumerate(puntas_dedos):
                dibujar_rectangulo_y_texto(frame, punto_dedo)
              
                    
                    
                
            
                distancia_gordo = calcular_distancia(puntas_dedos[0], landmarks.landmark[mp_manos.HandLandmark.WRIST])
                
                distancia_indice_palma = calcular_distancia(puntas_dedos[1], landmarks.landmark[mp_manos.HandLandmark.WRIST])
                
                distancia_middele = calcular_distancia(puntas_dedos[2], landmarks.landmark[mp_manos.HandLandmark.WRIST])
                
                distancia_anular = calcular_distancia(puntas_dedos[3], landmarks.landmark[mp_manos.HandLandmark.WRIST])
                
                distancia_pinky = calcular_distancia(puntas_dedos[4], landmarks.landmark[mp_manos.HandLandmark.WRIST])

               

                distancia_gordo = redondear_distancia(distancia_gordo)
                distancia_indice_palma = redondear_distancia(distancia_indice_palma)
                distancia_middele = redondear_distancia(distancia_middele)
                distancia_anular = redondear_distancia(distancia_anular)
                distancia_pinky = redondear_distancia(distancia_pinky)

                if time.time() - last_send_time > 1.0:
                  
                    if distancia_gordo > umbral_cierre:
                        print("\033[91m" + "gordo levantado" + "\033[0m")
                        # arduino.write(b'1')
                    else:
                        print("\033[92m" + "gordo abajo " + "\033[0m")
                        # arduino.write(b'2')

                    if distancia_pinky > umbral_cierre:
                        print("\033[91m" + "pinky levantado" + "\033[0m")
                    else:
                        print("\033[92m" + "pinky medio abajo " + "\033[0m")

                    if distancia_middele > umbral_cierre:
                        print("\033[91m" + "Dedo medio levantado" + "\033[0m")
                        # arduino.write(b'4')
                    else:
                        print("\033[92m" + "Dedo medio abajo " + "\033[0m")
                        # arduino.write(b'3')

                    if distancia_indice_palma > umbral_cierre:
                        print("\033[91m" + "indice levantado" + "\033[0m")
                        # arduino.write(b'5')
                    else:
                        print("\033[92m" + "indice abajo " + "\033[0m")
                        # arduino.write(b'6')

                    if distancia_anular > umbral_cierre:
                        print("\033[91m" + "Anular levantado" + "\033[0m \n" )
                        # arduino.write(b'8')
                    else:
                        print("\033[92m" + "Anular abajo " + "\033[0m \n" )
                        
                        
                        # arduino.write(b'7')
                      

                    last_send_time = time.time()

        cv2.imshow("Manos", frame)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
# ---------------------------------------------
# Cierre de la conexión con Arduino
# ---------------------------------------------
# arduino.close()

