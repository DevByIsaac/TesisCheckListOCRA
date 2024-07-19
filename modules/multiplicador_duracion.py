import json

def calcular_multiplicador_duracion(duracion_exposicion_minutos):
    """
    Calcula el Multiplicador de Duración (MD) basado en la duración de exposición a la tarea.
    
    Parámetros:
    duracion_exposicion_minutos (float): Duración total de la exposición a la tarea en minutos.
    
    Retorna:
    float: El Multiplicador de Duración (MD).
    """
    if duracion_exposicion_minutos <= 30:
        return 1.0
    elif 30 < duracion_exposicion_minutos <= 60:
        return 1.5
    elif 60 < duracion_exposicion_minutos <= 120:
        return 2.0
    elif 120 < duracion_exposicion_minutos <= 240:
        return 2.5
    else:
        return 3.0

def main(duracion_exposicion_minutos, output_json_path):
    md = calcular_multiplicador_duracion(duracion_exposicion_minutos)
    
    resultado = {
        'multiplicador_duracion': md
    }
    
    with open(output_json_path, 'w') as json_file:
        json.dump(resultado, json_file, indent=4)

if __name__ == "__main__":
    duracion_exposicion_minutos = 90  # Ejemplo: 90 minutos de exposición
    output_json_path = 'resultado_md.json'
    main(duracion_exposicion_minutos, output_json_path)
