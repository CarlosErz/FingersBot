
class image_processing:

    def __init__(self, puerto_com, camara, get_ports, active_arduino):
        self.puerto_com = puerto_com
        self.camara = camara
        self.get_ports = get_ports
        self.active_arduino = active_arduino

    def hands_funcion(self):
        import cv2
        import mediapipe as mp
        import serial
        import time
        import math
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        cap = cv2.VideoCapture(int(self.camara))

        if self.active_arduino == "on":
            try:
                arduino = serial.Serial(self.puerto_com, 9600)
                print("Conexión con Arduino establecida.")
            except serial.serialutil.SerialException as e:
                print(f"Error al abrir el puerto COM: {e}")
                arduino = None
        else:
            arduino = None
            print("La comunicación con Arduino está desactivada.")

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
            distancia_dedo = calcular_distancia(punto_dedo, landmarks.landmark[mp_hands.HandLandmark.WRIST])
            distancia_dedo = redondear_distancia(distancia_dedo)
            cv2.putText(frame, f"{distancia_dedo}", (x - 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_texto, 2)

        with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            prev_puntas_dedos = [None, None, None, None, None]
            last_send_time = time.time()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    continue

                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resultados = hands.process(frame_rgb)

                cv2.putText(frame, f"@Eanz para cerrar presiona Q", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                if resultados.multi_hand_landmarks:
                    for landmarks in resultados.multi_hand_landmarks:
                        puntas_dedos = [
                            landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
                            landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                            landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                            landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                            landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                        ]

                        umbral_cierre = 0.19
                        umbral_cierre_gordo = 18

                        acciones_dedos = {
                            'gordo': '0',
                            'pinky': '0',
                            'medio': '0',
                            'indice': '0',
                            'anular': '0'
                        }

                        for i, punto_dedo in enumerate(puntas_dedos):
                            dibujar_rectangulo_y_texto(frame, punto_dedo)

                            distancia_gordo = calcular_distancia(puntas_dedos[0], landmarks.landmark[mp_hands.HandLandmark.WRIST])
                            distancia_indice_palma = calcular_distancia(puntas_dedos[1], landmarks.landmark[mp_hands.HandLandmark.WRIST])
                            distancia_middele = calcular_distancia(puntas_dedos[2], landmarks.landmark[mp_hands.HandLandmark.WRIST])
                            distancia_anular = calcular_distancia(puntas_dedos[3], landmarks.landmark[mp_hands.HandLandmark.WRIST])
                            distancia_pinky = calcular_distancia(puntas_dedos[4], landmarks.landmark[mp_hands.HandLandmark.WRIST])

                            distancia_gordo = distancia_gordo * 100
                            distancia_indice_palma = redondear_distancia(distancia_indice_palma)
                            distancia_middele = redondear_distancia(distancia_middele)
                            distancia_anular = redondear_distancia(distancia_anular)
                            distancia_pinky = redondear_distancia(distancia_pinky)

                            if distancia_gordo <= umbral_cierre_gordo:
                                acciones_dedos['gordo'] = '1'
                            if distancia_indice_palma <= umbral_cierre:
                                acciones_dedos['indice'] = '1'
                            if distancia_middele <= umbral_cierre:
                                acciones_dedos['medio'] = '1'
                            if distancia_anular <= umbral_cierre:
                                acciones_dedos['anular'] = '1'
                            if distancia_pinky <= umbral_cierre:
                                acciones_dedos['pinky'] = '1'
                            if arduino:
                                arduino.write(f"{acciones_dedos['gordo']}{acciones_dedos['indice']}{acciones_dedos['medio']}{acciones_dedos['anular']}{acciones_dedos['pinky']}".encode())

                            print(f"{acciones_dedos['gordo']}{acciones_dedos['indice']}{acciones_dedos['medio']}{acciones_dedos['anular']}{acciones_dedos['pinky']}")

                cv2.imshow("FingersBot", frame)

                if cv2.waitKey(10) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()

        if arduino:
            arduino.close()

