import json

def cargar_datos_json(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def calcular_factor_fuerza(datos):
    fuerza_aplicada = datos['fuerza_aplicada']
    
    # Definir la fórmula para calcular el Factor de Fuerza (FFz)
    # Suponiendo que FFz = fuerza_aplicada / 50 (esto es solo un ejemplo; ajusta según la fórmula real que uses)
    FFz = fuerza_aplicada / 50
    
    return FFz

def obtener_datos_fuerza(json_path):
    datos = cargar_datos_json(json_path)
    
    # Suponiendo que la estructura del JSON es como sigue:
    # {
    #     "fuerza_aplicada": valor
    # }
    fuerza_aplicada = datos.get('fuerza_aplicada', 0)
    
    return {
        'fuerza_aplicada': fuerza_aplicada
    }

def guardar_resultados(json_path, resultado):
    with open(json_path, 'w') as json_file:
        json.dump(resultado, json_file, indent=4)

def main(input_json_path, output_json_path):
    datos = obtener_datos_fuerza(input_json_path)
    FFz = calcular_factor_fuerza(datos)
    
    resultado = {
        'factor_fuerza': FFz
    }
    
    guardar_resultados(output_json_path, resultado)

if __name__ == "__main__":
    input_json_path = 'ruta/al/archivo_entrada.json'
    output_json_path = 'ruta/al/archivo_salida.json'
    main(input_json_path, output_json_path)