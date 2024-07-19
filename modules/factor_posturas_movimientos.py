import json

def cargar_datos_json(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def calcular_factor_posturas_movimientos(datos):
    angulos = datos['angulos']
    
    # Definir la fórmula para calcular el Factor de Posturas y Movimientos (FP)
    # Aquí debes ajustar según las reglas específicas de OCRA para FP.
    
    # Suponiendo que calculamos FP como una media ponderada de los ángulos
    angulos = [
        datos['angulo_hombro_izquierdo'],
        datos['angulo_del_hombro_derecho'],
        datos['angulo_codo_izquierdo'],
        datos['angulo_codo_derecho'],
        datos['angulo_de_muneca_izquierda'],
        datos['angulo_de_muneca_derecha'],
        datos['angulo_mano_izquierdo'],
        datos['angulo_mano_derecho']
    ]
    
    if not angulos:
        return 0
    
    # Ejemplo de cálculo simple: Media aritmética de los ángulos
    FP = sum(angulos) / len(angulos)
    
    return FP

def obtener_datos_posturas_movimientos(json_path):
    datos = cargar_datos_json(json_path)
    
    return {
        'angulo_hombro_izquierdo': datos.get('angulo_hombro_izquierdo', 0),
        'angulo_del_hombro_derecho': datos.get('angulo_del_hombro_derecho', 0),
        'angulo_codo_izquierdo': datos.get('angulo_codo_izquierdo', 0),
        'angulo_codo_derecho': datos.get('angulo_codo_derecho', 0),
        'angulo_de_muneca_izquierda': datos.get('angulo_de_muneca_izquierda', 0),
        'angulo_de_muneca_derecha': datos.get('angulo_de_muneca_derecha', 0),
        'angulo_mano_izquierdo': datos.get('angulo_mano_izquierdo', 0),
        'angulo_mano_derecho': datos.get('angulo_mano_derecho', 0)
    }

def guardar_resultados(json_path, resultado):
    with open(json_path, 'w') as json_file:
        json.dump(resultado, json_file, indent=4)

def main(input_json_path, output_json_path):
    datos = obtener_datos_posturas_movimientos(input_json_path)
    FP = calcular_factor_posturas_movimientos(datos)
    
    resultado = {
        'factor_posturas_movimientos': FP
    }
    
    guardar_resultados(output_json_path, resultado)

if __name__ == "__main__":
    input_json_path = 'ruta/al/archivo_entrada.json'
    output_json_path = 'ruta/al/archivo_salida.json'
    main(input_json_path, output_json_path)