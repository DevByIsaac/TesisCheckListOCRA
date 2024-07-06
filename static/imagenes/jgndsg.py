#PoseModule
import cv2
import mediapipe as mp
import math

class poseDetector():

    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()

    def diferencia_dist(self, list):
        coordenadas =[]
        oreja_right = list[8][1:3]
        x1, y1 = oreja_right
        oreja_left = list[7][1:3]
        x2, y2 = oreja_left

        hombro_right = list[12][1:3]
        x3, y3 = hombro_right
        hombro_left = list[11][1:3]
        x4, y4 = hombro_left

        ojo_right = list[5][1:3]
        x5, y5 = ojo_right
        ojo_left = list[2][1:3]
        x6, y6 = ojo_left

        cedara_right = list[24][1:3]
        x7, y7 = cedara_right
        cadera_left = list[23][1:3]
        x8, y8 = cadera_left

        tobillo_right = list[28][1:3]
        x9, y9 = tobillo_right
        tobillo_left = list[27][1:3]
        x10, y10 = tobillo_left

        #inclinacion lateral cuello, oreja-hombro
        distancia_right_1 = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)
        distancia_left_1 = math.sqrt((x4 - x2)**2 + (y4 - y2)**2)
        incli_lat_cue = abs(distancia_right_1 - distancia_left_1)

        #rotacion cuello, ojo-hombro
        distancia_right_2 = math.sqrt((x3 - x5)**2 + (y3 - y5)**2)
        distancia_left_2 = math.sqrt((x4 - x6)**2 + (y4 - y6)**2)
        rotac_cue = abs(distancia_right_2 - distancia_left_2)        
        
        #inclinacion lateral tronco, hombro-cadera
        distancia_right_3 = math.sqrt((x3 - x7)**2 + (y3 - y7)**2)
        distancia_left_3 = math.sqrt((x4 - x8)**2 + (y4 - y8)**2)
        incli_lat_tron = abs(distancia_right_3 - distancia_left_3)
        
        #rotacion tronco, hombro-cadera
        distancia_right_4 = math.sqrt((x3 - x8)**2 + (y3 - y8)**2)
        distancia_left_4 = math.sqrt((x4 - x7)**2 + (y4 - y7)**2)
        rotac_tron = abs(distancia_right_4 - distancia_left_4)

        #pie alzado, cadera-tobillo
        distancia_right_5 = math.sqrt((x7 - x9)**2 + (y7 - y9)**2)
        distancia_left_5 = math.sqrt((x8 - x10)**2 + (y8 - y10)**2)
        pie_alzado = abs(distancia_right_5 - distancia_left_5)

        coordenadas.append((incli_lat_cue, rotac_cue, incli_lat_tron, rotac_tron, pie_alzado))
        return coordenadas  # Si la diferencia es mayor, devuelve 2


    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        h, w, c = img.shape
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                #h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)                
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList    

    # Calculate angle.
    def findAngle3(self, x1, y1, x2, y2):    
        # Verifica si el denominador es cero
        if y1 == 0 or (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1) == 0:            
            return None  # Puedes devolver un valor especial según tus necesidades
        else:
            theta = math.acos((y2 - y1) * (-y1) / (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
            degree = int(180 / math.pi) * theta
            return degree

    def findAngle(self, img, p1, p2, p3, draw=True):
    # Get the landmarks
        if self.results.pose_landmarks:
            lm_list = self.results.pose_landmarks.landmark

            if all(lm_list[i].visibility > 0.5 for i in [p1, p2, p3]):
                points = [(int(lm_list[i].x * img.shape[1]), int(lm_list[i].y * img.shape[0])) for i in [p1, p2, p3]]
                #points = [(lm_list[i].x, lm_list[i].y) for i in [p1, p2, p3]]
                
                # Calculate vectors
                v1 = (points[0][0] - points[1][0], points[0][1] - points[1][1])
                v2 = (points[2][0] - points[1][0], points[2][1] - points[1][1])

                # Calculate dot product and magnitudes
                dot_product = v1[0] * v2[0] + v1[1] * v2[1]
                magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
                magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

                # Calculate angle in radians
                theta = math.acos(dot_product / (magnitude_v1 * magnitude_v2))

                # Convert angle to degrees
                angle1 = math.degrees(theta)

                # Calculate the Angle
                angle = math.degrees(math.atan2(points[2][1] - points[1][1], points[2][0] - points[1][0]) -
                                    math.atan2(points[0][1] - points[1][1], points[0][0] - points[1][0]))

                if draw:
                    cv2.line(img, points[0], points[1], (255, 255, 255), 2)
                    cv2.line(img, points[2], points[1], (255, 255, 255), 2)
                    cv2.circle(img, points[0], 5, (0, 0, 255), cv2.FILLED)                    
                    cv2.circle(img, points[1], 5, (0, 0, 255), cv2.FILLED)                    
                    cv2.circle(img, points[2], 5, (0, 0, 255), cv2.FILLED)                    
                    cv2.putText(img, str(int(angle1)), (points[1][0] + 10, points[1][1]), cv2.FONT_HERSHEY_PLAIN, 0.9,
                                (0, 255, 0), 2)

                return angle1

        return None

    
    def evaluar_postura_REBA(self, angulos, compara):
        # Aquí debes implementar las reglas específicas del método REBA
        #GRUPO A
        
        #Cuello
        puntaje_inclinacion_cuello = 0        
        # Verifica que los ángulos sean diferentes de None antes de comparar
        if angulos["Inclinacion del cuello"] is not None:
            if angulos["Inclinacion del cuello"] <= 20:
                puntaje_inclinacion_cuello = 1  # Puedes ajustar este valor según tu criterio                
            else:
                puntaje_inclinacion_cuello = 2
            
            for puntajes in compara:
                incli_lat_cuello, rotacion_cuello, in_lat_tron, rota_tron, pie_alza = puntajes    
                print(puntajes)
                if ((incli_lat_cuello >= 30) or (rotacion_cuello >= 30)):
                    puntaje_inclinacion_cuello += 1                    
        
        #Tronco
        puntaje_inclinacion_tronco = 0        
        if angulos["Inclinacion del torso"] == 0:
            puntaje_inclinacion_tronco = 1  # Puedes ajustar este valor según tu criterio
        elif 0 < angulos["Inclinacion del torso"] <= 20:
            puntaje_inclinacion_tronco = 2
        elif 20 < angulos["Inclinacion del torso"] <= 60:
            puntaje_inclinacion_tronco = 3
        else:
            puntaje_inclinacion_tronco = 4
        
        if ((in_lat_tron >= 30) or (rota_tron >= 30)):
            puntaje_inclinacion_tronco += 1            

        #Piernas
        puntaje_piernas = 0                
        # Verificar si la persona está de pie o sentada con soporte bilateral
        # Lista de lados a considerar (izquierdo y derecho)
        lados = ["Izquierda", "Derecha"]
        puntajes_lista_a = []
        for lado in lados:            
            cadera_key = f"Cadera {lado}"
            rodilla_key = f"Rodilla {lado}"

            # Verificar si la persona está de pie o sentada con soporte bilateral
            if ((angulos[cadera_key] is not None) and (
                (93 > angulos[cadera_key] >87 ) and (0 <= angulos["Inclinacion del torso"] <= 30))):

                puntaje_piernas = 1

                # Sumar 1 punto si hay flexión de rodillas entre 30 y 60 grados
                if angulos[rodilla_key] is not None:
                    if 120 <= angulos[rodilla_key] <= 150:
                        puntaje_piernas += 1

                    # Sumar 2 puntos si las rodillas están flexionadas más de 60 grados
                    elif angulos[rodilla_key] < 120:
                        puntaje_piernas += 2
            elif ((0 <= angulos[rodilla_key] <= 30) and(
                155 < angulos[cadera_key])):
                puntaje_piernas = 1
                # Sumar 1 punto si hay flexión de rodillas entre 30 y 60 grados
                if angulos[rodilla_key] is not None:
                    if 120 <= angulos[rodilla_key] <= 150:
                        puntaje_piernas += 1

                    # Sumar 2 puntos si las rodillas están flexionadas más de 60 grados
                    elif angulos[rodilla_key] < 120:
                        puntaje_piernas += 2
            # Verificar si la persona tiene soporte unilateral (de pie)
            elif angulos[cadera_key] is not None and (
                angulos[cadera_key] < 160 and pie_alza > 50):
                puntaje_piernas = 2
                print(f"Pie alzado: {pie_alza}")

                # Sumar 1 punto si hay flexión de rodillas entre 30 y 60 grados
                if angulos[rodilla_key] is not None:
                    if 120 <= angulos[rodilla_key] <= 150:
                        puntaje_piernas += 1

                    # Sumar 2 puntos si las rodillas están flexionadas más de 60 grados
                    elif angulos[rodilla_key] < 120:
                        puntaje_piernas += 2
            #puntaje_total = puntaje_piernas + puntaje_inclinacion_tronco + puntaje_inclinacion_cuello
            puntajes_lista_a.append((puntaje_inclinacion_cuello, puntaje_piernas, puntaje_inclinacion_tronco))

            return puntajes_lista_a

    def obtener_puntuacion_ga(self, puntajes_lista_a):
        # Definir la matriz de calificación
        matriz_calificacion = [
            [1, 2, 3, 4, 1, 2, 3, 4, 3, 3, 5, 6],
            [2, 3, 4, 5, 3, 4, 5, 6, 4, 5, 6, 7],
            [2, 4, 5, 6, 4, 5, 6, 7, 5, 6, 7, 8],
            [3, 5, 6, 7, 5, 6, 7, 8, 6, 7, 8, 9],
            [4, 6, 7, 8, 6, 7, 8, 9, 7, 8, 9, 9]
        ]

        # Verificar que los puntajes estén dentro del rango permitido
        for puntajes in puntajes_lista_a:
            cuello, piernas, tronco = puntajes
            if 1 <= cuello <= 3 and 1 <= piernas <= 4 and 1 <= tronco <= 5:
                # Obtener la puntuación según las conexiones en la matriz
                puntuacion = matriz_calificacion[tronco - 1][4 * (cuello - 1) + (piernas - 1)]
                #print(f"Puntuación para {puntajes}: {puntuacion}")
                return puntuacion
            else:
                print(f"Puntajes inválidos para {puntajes}")

    
    def evaluar_postura_REBAB(self, angulos):
        # Aquí debes implementar las reglas específicas del método REBA
        #GRUPO B        
        #Brazo
        puntaje_brazos = 0                       
        # Lista de lados a considerar (izquierdo y derecho)
        lados = ["Derecho", "Izquierdo"]
        puntajes_lista_b = []
        for lado in lados:            
            hombro_key = f"Hombro {lado}"
            codo_key = f"Codo {lado}"
            
            if angulos[hombro_key] is not None:
                if angulos[hombro_key] <= 20:
                    puntaje_brazos = 1
                
                elif (20 < angulos[hombro_key] <= 45):
                    puntaje_brazos = 2

                elif 45 < angulos[hombro_key] <= 90:
                    puntaje_brazos = 3

                elif angulos[hombro_key] > 90:
                    puntaje_brazos = 4            
        #Antebrazo
            puntaje_codos = 0
            if angulos[codo_key] is not None:
                if 120 >= angulos[codo_key] >= 80:
                    puntaje_codos = 1
                
                elif (angulos[codo_key]> 120) or (angulos[codo_key] < 80):
                    puntaje_codos = 2
        #Muñeca
        puntaje_muñecas = 0
        lados1 = ["Izquierda", "Derecha"]        
        for lado1 in lados1:            
            muñeca_key = f"Muñeca {lado1}"                        
            
            if angulos[muñeca_key] is not None:
                if angulos[muñeca_key] >= 165:
                    puntaje_muñecas = 1
                
                elif (angulos[muñeca_key] < 165):
                    puntaje_muñecas = 2


            puntajes_lista_b.append((puntaje_codos, puntaje_muñecas, puntaje_brazos,))

            return puntajes_lista_b
        
    def obtener_puntuacion_gb(self, puntajes_lista_b):
        # Definir la matriz de calificación
        matriz_calificacion_gb = [
            [1, 2, 2, 1, 2, 3],
            [1, 2, 3, 2, 3, 4],
            [3, 4, 5, 4, 5, 5],
            [4, 5, 5, 5, 6, 7],
            [6, 7, 8, 7, 8, 8],
            [7, 8, 8, 8, 9, 9]
        ]

        # Verificar que los puntajes estén dentro del rango permitido
        for puntajes in puntajes_lista_b:
            antebrazo, muñeca, brazo = puntajes
            if 1 <= antebrazo <= 2 and 1 <= muñeca <= 3 and 1 <= brazo <= 6:
                # Obtener la puntuación según las conexiones en la matriz
                puntuacion = matriz_calificacion_gb[brazo-1][3 * (antebrazo - 1) + (muñeca - 1)]
                #print(f"Puntuación para {puntajes}: {puntuacion}")
                return puntuacion
            else:
                print(f"Puntajes inválidos para {puntajes}")

    def obtener_puntuacion_tc(self, puntuacion_a, puntuacion_b):        
        # Definir la matriz de calificación
        matriz_calificacion_tc = [
            [1, 1, 1, 2, 3, 3, 4, 5, 6, 7, 7, 7],
            [1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8],
            [2, 3, 3, 3, 4, 5, 6, 7, 7, 8, 8, 8],
            [3, 4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9],
            [4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9, 9],
            [6, 6, 6, 7, 8, 8, 9, 9, 10, 10, 10, 10],
            [7, 7, 7, 8, 9, 9, 9, 10, 10, 11, 11, 11],
            [8, 8, 8, 9, 10, 10, 10, 10, 10, 11, 11, 11],
            [9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12],
            [10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 12],
            [11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12],
            [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
        ]

        # Verificar que los puntajes estén dentro del rango permitido        
        if puntuacion_a is not None and puntuacion_b is not None:
            if 1 <= puntuacion_a <= 12 and 1 <= puntuacion_b <= 12:
                # Obtener la puntuación según las conexiones en la matriz
                puntuacion = matriz_calificacion_tc[puntuacion_a-1][puntuacion_b-1]
                #print(f"Puntuación para ({puntuacion_a}, {puntuacion_b}): {puntuacion}")
                return puntuacion
            else:
                print(f"Puntajes inválidos para ({puntuacion_a}, {puntuacion_b})")

    def obtener_resultado(self, puntuacion_tc):        
        # Definir las variables de calificación        
        nivel_accion = 0
        nivel_riesgo = ""
        intervencion = ""
        lista_resultados = []

        # Verificar que los puntajes estén dentro del rango permitido        
        if puntuacion_tc is not None:
            if puntuacion_tc == 1:
                # Obtener la puntuación según las conexiones en la matriz
                nivel_accion = 0
                nivel_riesgo = "Inapreciable"
                intervencion = "No necesario"
                
            elif 2 <= puntuacion_tc <= 3:
                nivel_accion = 1
                nivel_riesgo = "Bajo"
                intervencion = "Puede ser necesario"
                
            elif 4 <= puntuacion_tc <= 7:
                nivel_accion = 2
                nivel_riesgo = "Medio"
                intervencion = "Necesario"
                
            elif 8 <= puntuacion_tc <= 10:
                nivel_accion = 3
                nivel_riesgo = "Alto"
                intervencion = "Necesario Pronto"
                
            elif 11 <= puntuacion_tc <= 15:
                nivel_accion = 4
                nivel_riesgo = "Muy Alto"
                intervencion = "Actuación Inmediata"
            lista_resultados.append((nivel_accion, nivel_riesgo, intervencion))
            return lista_resultados
    