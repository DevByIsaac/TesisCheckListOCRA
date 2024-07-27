import json
import os
import glob

def calcular_md(tntr):
    """
    Calcula el Multiplicador de Duración (MD) basado en el Tiempo Neto de Trabajo Repetitivo (TNTR).
    
    :param tntr: Tiempo Neto de Trabajo Repetitivo en minutos
    :return: Puntuación del Multiplicador de Duración (MD)
    """
    if tntr <= 60:
        return 0.5
    elif 60 < tntr <= 120:
        return 0.5
    elif 120 < tntr <= 180:
        return 0.65
    elif 180 < tntr <= 240:
        return 0.75
    elif 240 < tntr <= 300:
        return 0.85
    elif 300 < tntr <= 360:
        return 0.925
    elif 360 < tntr <= 420:
        return 0.95
    elif 420 < tntr <= 480:
        return 1
    elif 480 < tntr <= 539:
        return 1.2
    elif 539 < tntr <= 599:
        return 1.5
    elif 599 < tntr <= 659:
        return 2
    elif 659 < tntr <= 719:
        return 2.8
    elif tntr >= 720:
        return 4
    else:  # Para análisis multitarea
        if tntr <= 1.87:
            return 0.01
        elif 1.87 < tntr <= 3.75:
            return 0.02
        elif 3.75 < tntr <= 7.5:
            return 0.05
        elif 7.5 < tntr <= 15:
            return 0.1
        elif 15 < tntr <= 30:
            return 0.2
        elif 30 < tntr <= 59:
            return 0.35

def get_most_recent_file(folder_path, extension):
    """Encuentra el archivo más reciente con la extensión dada en la carpeta especificada."""
    list_of_files = glob.glob(os.path.join(folder_path, '*' + extension))
    if not list_of_files:
        raise FileNotFoundError(f"No se encontraron archivos con la extensión {extension} en {folder_path}.")
    return max(list_of_files, key=os.path.getmtime)

def main():
    # Definir la carpeta donde están los archivos JSON
    json_folder = 'C:/Tesis/TestErgo/archivos_json'
    json_path = get_most_recent_file(json_folder, '.json')

    # Leer el archivo JSON
    with open(json_path, 'r') as file:
        data_list = json.load(file)

    # Verificar si data_list es una lista y si no está vacía
    if not isinstance(data_list, list) or len(data_list) == 0:
        raise ValueError("El archivo JSON no contiene una lista válida o está vacío.")

    # Tomar el primer objeto de la lista
    data = data_list[0]

    # Extraer TNTR del JSON
    tntr = data.get('TNTR', 480)  # Usar 480 minutos por defecto si no está presente

    # Calcular el MD
    md = calcular_md(tntr)

    # Añadir el cálculo al JSON
    data['Multiplicador de Duracion'] = md

    # Guardar el JSON actualizado
    updated_json_path = json_path.replace('.json', '_md.json')
    with open(updated_json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

    print(f"El JSON se ha actualizado con el Multiplicador de Duración y guardado en {updated_json_path}.")

if __name__ == "__main__":
    main()
