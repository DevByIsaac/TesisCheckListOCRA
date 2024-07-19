import json

def cargar_datos_json(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def calcular_factor_recuperacion(datos):
    pausas = datos['pausas']
    duracion_turno = datos['duracion_turno']
    
    # Sumar la duración total de las pausas
    duracion_total_pausas = sum(pausa['duracion'] for pausa in pausas)
    
    # Calcular el Factor de Recuperación (FR)
    FR = duracion_total_pausas / duracion_turno
    
    return FR

def obtener_datos_pausas_y_turno(json_path):
    datos = cargar_datos_json(json_path)
    
    # Suponiendo que la estructura del JSON es como sigue:
    # {
    #     "pausas": [
    #         {"inicio": "HH:MM:SS", "fin": "HH:MM:SS", "duracion": segundos},
    #         ...
    #     ],
    #     "duracion_turno": segundos
    # }
    pausas = datos.get('pausas', [])
    duracion_turno = datos.get('duracion_turno', 0)
    
    return {
        'pausas': pausas,
        'duracion_turno': duracion_turno
    }

def guardar_resultados(json_path, resultado):
    with open(json_path, 'w') as json_file:
        json.dump(resultado, json_file, indent=4)

def main(input_json_path, output_json_path):
    datos = obtener_datos_pausas_y_turno(input_json_path)
    FR = calcular_factor_recuperacion(datos)
    
    resultado = {
        'factor_recuperacion': FR
    }
    
    guardar_resultados(output_json_path, resultado)

if __name__ == "__main__":
    input_json_path = 'ruta/al/archivo_entrada.json'
    output_json_path = 'ruta/al/archivo_salida.json'
    main(input_json_path, output_json_path)
