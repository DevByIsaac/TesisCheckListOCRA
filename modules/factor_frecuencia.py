import json

def cargar_datos_json(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def calcular_factor_frecuencia(datos):
    ciclos_por_minuto = datos['ciclos_por_minuto']
    
    # Definir la fórmula para calcular el Factor de Frecuencia (FF)
    # Suponiendo que FF = ciclos_por_minuto / 10 (esto es solo un ejemplo; ajusta según la fórmula real que uses)
    FF = ciclos_por_minuto / 10
    
    return FF

def obtener_datos_ciclos(json_path):
    datos = cargar_datos_json(json_path)
    
    # Suponiendo que la estructura del JSON es como sigue:
    # {
    #     "ciclos_por_minuto": valor
    # }
    ciclos_por_minuto = datos.get('ciclos_por_minuto', 0)
    
    return {
        'ciclos_por_minuto': ciclos_por_minuto
    }

def guardar_resultados(json_path, resultado):
    with open(json_path, 'w') as json_file:
        json.dump(resultado, json_file, indent=4)

def main(input_json_path, output_json_path):
    datos = obtener_datos_ciclos(input_json_path)
    FF = calcular_factor_frecuencia(datos)
    
    resultado = {
        'factor_frecuencia': FF
    }
    
    guardar_resultados(output_json_path, resultado)

if __name__ == "__main__":
    input_json_path = 'ruta/al/archivo_entrada.json'
    output_json_path = 'ruta/al/archivo_salida.json'
    main(input_json_path, output_json_path)