import json

def cargar_datos_json(json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def calcular_factor_riesgos_adicionales(datos):
    # Definir factores adicionales que pueden influir en el FC
    riesgo_herramienta = datos.get('riesgo_herramienta', 0)
    riesgo_movimiento_repetitivo = datos.get('riesgo_movimiento_repetitivo', 0)
    condiciones_ambientales = datos.get('condiciones_ambientales', 0)
    
    # Ejemplo de cálculo simple para el Factor de Riesgos Adicionales (FC)
    # Puedes ajustar la fórmula según las necesidades específicas del análisis OCRA
    FC = riesgo_herramienta + riesgo_movimiento_repetitivo + condiciones_ambientales
    
    return FC

def obtener_datos_riesgos_adicionales(json_path):
    datos = cargar_datos_json(json_path)
    
    return {
        'riesgo_herramienta': datos.get('riesgo_herramienta', 0),
        'riesgo_movimiento_repetitivo': datos.get('riesgo_movimiento_repetitivo', 0),
        'condiciones_ambientales': datos.get('condiciones_ambientales', 0)
    }

def guardar_resultados(json_path, resultado):
    with open(json_path, 'w') as json_file:
        json.dump(resultado, json_file, indent=4)

def main(input_json_path, output_json_path):
    datos = obtener_datos_riesgos_adicionales(input_json_path)
    FC = calcular_factor_riesgos_adicionales(datos)
    
    resultado = {
        'factor_riesgos_adicionales': FC
    }
    
    guardar_resultados(output_json_path, resultado)

if __name__ == "__main__":
    input_json_path = 'ruta/al/archivo_entrada.json'
    output_json_path = 'ruta/al/archivo_salida.json'
    main(input_json_path, output_json_path)