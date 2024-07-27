import json
import os
import glob

def calcular_ffz(acciones):
    """
    Calcula el Factor de Fuerza (FFz) basado en las acciones que requieren fuerza.
    
    :param acciones: Lista de acciones que requieren fuerza con sus detalles
    :return: Puntuación del Factor de Fuerza (FFz)
    """
    puntuacion_total = 0
    
    for accion in acciones:
        esfuerzo = accion['esfuerzo_cr10']
        duracion = accion['duracion']
        
        if esfuerzo in [3, 4]:  # Fuerza Moderada
            if duracion == "1/3 del tiempo":
                puntuacion_total += 2
            elif duracion == "50% del tiempo":
                puntuacion_total += 4
            elif duracion == "> 50% del tiempo":
                puntuacion_total += 6
            elif duracion == "Casi todo el tiempo":
                puntuacion_total += 8
                
        elif esfuerzo in [5, 6]:  # Fuerza Intensa
            if duracion == "2 seg. cada 10 min.":
                puntuacion_total += 4
            elif duracion == "1% del tiempo":
                puntuacion_total += 8
            elif duracion == "5% del tiempo":
                puntuacion_total += 16
            elif duracion == "> 10% del tiempo":
                puntuacion_total += 24
        
        elif esfuerzo >= 7:  # Fuerza Casi Máxima
            if duracion == "2 seg. cada 10 min.":
                puntuacion_total += 6
            elif duracion == "1% del tiempo":
                puntuacion_total += 12
            elif duracion == "5% del tiempo":
                puntuacion_total += 24
            elif duracion == "> 10% del tiempo":
                puntuacion_total += 32
    
    return puntuacion_total

def mostrar_menu():
    """
    Muestra un menú con opciones predefinidas para ingresar datos.
    
    :return: Lista de acciones con sus detalles según la opción seleccionada
    """
    opciones = {
        1: {'esfuerzo_cr10': 3, 'duracion': "1/3 del tiempo"},
        2: {'esfuerzo_cr10': 4, 'duracion': "50% del tiempo"},
        3: {'esfuerzo_cr10': 5, 'duracion': "2 seg. cada 10 min."},
        4: {'esfuerzo_cr10': 6, 'duracion': "1% del tiempo"},
        5: {'esfuerzo_cr10': 7, 'duracion': "5% del tiempo"},
        6: {'esfuerzo_cr10': 8, 'duracion': "> 10% del tiempo"}
    }
    
    acciones = []
    while True:
        print("\nSeleccione una acción para agregar:")
        for key, value in opciones.items():
            print(f"  {key}: Esfuerzo CR10 = {value['esfuerzo_cr10']}, Duración = {value['duracion']}")
        print("  0: Terminar")

        try:
            seleccion = int(input("Ingrese el número de la opción: "))
            if seleccion == 0:
                break
            if seleccion in opciones:
                acciones.append(opciones[seleccion])
            else:
                print("Opción inválida. Por favor, seleccione un número válido.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")
    
    return acciones

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

    # Intentar extraer acciones del JSON
    acciones = data.get('acciones_fuerza', None)

    # Si no están presentes en el JSON, pedir al usuario que seleccione las acciones del menú
    if acciones is None:
        print("No se encontraron acciones de fuerza en el archivo JSON.")
        acciones = mostrar_menu()

    # Calcular el FFz
    ffz = calcular_ffz(acciones)

    # Añadir el cálculo al JSON
    data['Factor de Fuerza'] = ffz

    # Guardar el JSON actualizado
    updated_json_path = json_path.replace('.json', '_ffz.json')
    with open(updated_json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

    print(f"El JSON se ha actualizado con el Factor de Fuerza y guardado en {updated_json_path}.")

if __name__ == "__main__":
    main()
