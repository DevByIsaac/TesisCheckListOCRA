import math, random
class evaluacion_rula():

    def rula_grupo_A(self, angulos, modi_antebra):
        # Aquí se implementa las reglas específicas del método RULA del GRUPO A
        #GRUPO A        
        #Brazo
        puntaje_brazos = 0
        puntaje_codos = 0                       
        # Lista de lados a considerar (izquierdo y derecho)
        lados = ["Izquierdo", "Derecho"]
        puntajes_lista_A = []
        for lado in lados:            
            hombro_key = f"Hombro {lado}"
            codo_key = f"Codo {lado}"
            modiante_key = f"Modiantebrazo {lado}"
            
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
            
            if angulos[codo_key] is not None:
                if 80 <= angulos[codo_key] <= 120:
                    print(angulos[codo_key])
                    puntaje_codos = 1
                
                elif (angulos[codo_key]> 120) or (angulos[codo_key] < 80):
                    print(angulos[codo_key])
                    puntaje_codos = 2
                #Aunmenta en 1
                if modi_antebra[modiante_key] is not None:
                    if (modi_antebra[modiante_key] > 140) or (modi_antebra[modiante_key] < 70):
                        puntaje_codos +=1
        #Muñeca
        puntaje_muñecas = 0
        lados1 = ["Izquierda", "Derecha"]        
        for lado1 in lados1:            
            muñeca_key = f"Muñeca {lado1}"

            
            if angulos[muñeca_key] is not None:
                if angulos[muñeca_key] == 180:
                    puntaje_muñecas = 1
                
                elif 180 > angulos[muñeca_key] >= 165:
                    puntaje_muñecas = 2

                elif (angulos[muñeca_key] < 165):
                    puntaje_muñecas = 3

        #Puntuación giro muñeca
        giro_muñeca = random.randint(1, 2)
        puntajes_lista_A.append((puntaje_brazos, puntaje_codos, puntaje_muñecas, giro_muñeca))

        return puntajes_lista_A
        
    def rula_puntuacion_gA(self, puntajes_lista_A):
        # Definir la matriz de calificación
        matriz_calificacion_gb = [
            [1, 2, 1, 2, 1, 2, 1, 2],
            [2, 2, 2, 2, 3, 3, 3, 3],
            [2, 3, 3, 3, 3, 3, 4, 4],
            [2, 3, 3, 3, 3, 4, 4, 4],
            [3, 3, 3, 3, 3, 4, 4, 4],
            [3, 4, 4, 4, 4, 4, 5, 5],
            [3, 3, 4, 4, 4, 4, 5, 5],
            [2, 4, 4, 4, 4, 4, 5, 5],
            [4, 4, 4, 4, 4, 5, 5, 5],
            [4, 4, 4, 4, 4, 5, 5, 5],
            [4, 4, 4, 4, 4, 5, 5, 5],
            [4, 4, 4, 5, 5, 5, 6, 6],
            [5, 5, 5, 5, 5, 6, 6, 7],
            [5, 6, 6, 6, 6, 7, 7, 7],
            [6, 6, 6, 7, 7, 7, 7, 8],
            [7, 7, 7, 7, 7, 8, 8, 9],
            [8, 8, 8, 8, 8, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
        ]

        # Verificar que los puntajes estén dentro del rango permitido
        for puntajes in puntajes_lista_A:
            brazo, antebrazo, muñeca, giro_muñeca = puntajes
            if 1 <= brazo <= 6 and 1 <= antebrazo <= 3 and 1 <= muñeca <= 4 and 1 <= giro_muñeca <= 2:
                # Obtener la puntuación según las conexiones en la matriz
                puntuacion = matriz_calificacion_gb[3*(brazo-1) + (antebrazo - 1)][2 * (muñeca - 1) + (giro_muñeca - 1)]
                print(f"Puntuación para {puntajes}: {puntuacion}")
                return puntuacion
            else:
                print(f"Puntajes inválidos para {puntajes}")
        
    
    def rula_grupo_B(self, angulos, compara):
        # Aquí se implementa las reglas específicas del método RULA del GRUPO B
        #GRUPO B
        #Cuello
        puntaje_inclinacion_cuello = 0        
        # Verifica que los ángulos sean diferentes de None antes de comparar
        if angulos["Inclinacion del cuello"] is not None:
            if 0 <= angulos["Inclinacion del cuello"] <= 10:
                puntaje_inclinacion_cuello = 1  # Puedes ajustar este valor según tu criterio
            elif 10 < angulos["Inclinacion del cuello"] <= 20:
                puntaje_inclinacion_cuello = 2
            elif 20 < angulos["Inclinacion del cuello"]:
                puntaje_inclinacion_cuello = 3
            
            for puntajes in compara:
                incli_lat_cuello, rotacion_cuello, in_lat_tron, rota_tron, pie_alza = puntajes    
                #print(puntajes)    
                if incli_lat_cuello >= 30:
                    puntaje_inclinacion_cuello += 1
                elif rotacion_cuello >= 30:
                    puntaje_inclinacion_cuello +=1
                    #print(puntaje_inclinacion_cuello)
        #Tronco
        puntaje_inclinacion_tronco = 0
        puntaje_piernas = 0                
        puntajes_lista_B = []
        # Lista de lados a considerar (izquierda y derecha)
        lados = ["Izquierda", "Derecha"]  
        for lado in lados:            
            cadera_key = f"Cadera {lado}"
            rodilla_key = f"Rodilla {lado}"

            if (angulos[cadera_key] is not None and ((angulos[rodilla_key] is not None)and (
                93 < angulos[rodilla_key] > 87))) and ((93 > angulos[cadera_key] >87 ) and (
                angulos["Inclinacion del torso"] == 0)):
                puntaje_inclinacion_tronco = 1 
            elif 0 < angulos["Inclinacion del torso"] <= 20:
                puntaje_inclinacion_tronco = 2
            elif 20 < angulos["Inclinacion del torso"] <= 60:
                puntaje_inclinacion_tronco = 3
            else:
                puntaje_inclinacion_tronco = 4
            
            if (in_lat_tron >= 30):
                puntaje_inclinacion_tronco += 1                
            elif (rota_tron >= 30):
                puntaje_inclinacion_tronco += 1
            

        #Piernas
            # Verificar si la persona está sentada
            if ((angulos[cadera_key] is not None) and (
                (93 > angulos[cadera_key] >87 ) and (0 <= angulos["Inclinacion del torso"] <= 30))):

                puntaje_piernas = 1                              
            
            # Verificar si la persona está de pie
            if angulos[cadera_key] is not None and (
                (160 <= angulos[cadera_key]) or (0 <= angulos[cadera_key] <= 100)):

                puntaje_piernas = 1

            # Verificar si la persona tiene soporte unilateral (de pie)
            elif angulos[cadera_key] is not None and (
                100 < angulos[cadera_key] < 160 or pie_alza > 40):
                puntaje_piernas = 2
                print(f"Pie alzado: {pie_alza}")

            if angulos["Cadera Derecha"] is not None:
                cadera_key = "Cadera Derecha"
                # Verificar si la persona está sentada
                if ((angulos[cadera_key] is not None) and (
                    (93 > angulos[cadera_key] >87 ) and (0 <= angulos["Inclinacion del torso"] <= 30))):

                    puntaje_piernas = 1                              
                
                # Verificar si la persona está de pie
                if angulos[cadera_key] is not None and (
                    (160 <= angulos[cadera_key]) or (0 <= angulos[cadera_key] <= 100)):

                    puntaje_piernas = 1

                # Verificar si la persona tiene soporte unilateral (de pie)
                elif angulos[cadera_key] is not None and (
                    100 < angulos[cadera_key] < 160 or pie_alza > 40):
                    puntaje_piernas = 2
                    print(f"Pie alzado: {pie_alza}")                
                
            puntajes_lista_B.append((puntaje_inclinacion_cuello, puntaje_inclinacion_tronco, puntaje_piernas))

            return puntajes_lista_B

    def rula_puntuacion_gB(self, puntajes_lista_B):
        # Definir la matriz de calificación
        matriz_calificacion = [
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            [1, 3, 2, 3, 3, 4, 5, 5, 6, 6, 7, 7],
            [2, 3, 2, 3, 4, 5, 5, 5, 6, 7, 7, 7],
            [5, 5, 5, 6, 6, 7, 7, 7, 7, 7, 8, 8],
            [7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 7, 8, 6, 8, 8, 9, 9, 9, 9, 9]
        ]

        # Verificar que los puntajes estén dentro del rango permitido
        for puntajes in puntajes_lista_B:
            cuello, tronco, piernas = puntajes
            if 1 <= cuello <= 6 and 1 <= tronco <= 6 and 1 <= piernas <= 2:
                # Obtener la puntuación según las conexiones en la matriz
                puntuacion = matriz_calificacion[cuello - 1][2 * (tronco - 1) + (piernas - 1)]
                print(f"Puntuación para {puntajes}: {puntuacion}")
                return puntuacion
            else:
                print(f"Puntajes inválidos para {puntajes}")

    
    def rula_puntuacion_tabla_C(self, puntuacion_a, puntuacion_b):        
        matriz_calificacion_tc = [
            [1, 2, 3, 3, 4, 5, 5, 5, 5],
            [2, 2, 3, 4, 4, 5, 5, 5, 5],
            [3, 3, 3, 4, 4, 5, 6, 6, 6],
            [3, 3, 3, 4, 5, 6, 6, 6, 6],
            [4, 4, 4, 5, 6, 7, 7, 7, 7],
            [4, 4, 5, 6, 6, 7, 7, 7, 7],
            [5, 5, 6, 6, 7, 7, 7, 7, 7],
            [5, 5, 6, 7, 7, 7, 7, 7, 7],
            [5, 5, 6, 7, 7, 7, 7, 7, 7]            
        ]

        # Verificar que los puntajes estén dentro del rango permitido        
        if puntuacion_a is not None and puntuacion_b is not None:
            if 1 <= puntuacion_a <= 9 and 1 <= puntuacion_b <= 9:
                # Obtener la puntuación según las conexiones en la matriz
                puntuacion = matriz_calificacion_tc[puntuacion_a-1][puntuacion_b-1]
                #print(f"Puntuación para ({puntuacion_a}, {puntuacion_b}): {puntuacion}")
                return puntuacion
            #else:
                #print(f"Puntajes inválidos para ({puntuacion_a}, {puntuacion_b})")

    def rula_resultado(self, puntuacion_tc):        
        # Definir las variables de calificación        
        nivel_accion = 0
        indicacion = ""        
        lista_resultados = []
        
        if puntuacion_tc is not None:
            if 1<= puntuacion_tc <=2:
                nivel_accion = 1
                indicacion = "Postura aceptable si no se repite o mantiene durante largos periodos"                
                
            elif 3 <= puntuacion_tc <= 4:
                nivel_accion = 2
                indicacion = "Necesidad de una evaluación mas detallada y posibilidad de requerir cambios"
                
            elif 5 <= puntuacion_tc <= 6:
                nivel_accion = 3
                indicacion = "Necesidad de efectuar un estudio en profundidad y corregir la postura lo antes posible"
                
            else:
                nivel_accion = 4
                indicacion = "Necesidad de corregir la postura inmediatamente"
            lista_resultados.append((nivel_accion, indicacion))
            return lista_resultados
