import json
import os
import glob

def calcular_ff(atd, ate):
    """
    Calcula el Factor de Frecuencia (FF) basado en las puntuaciones ATD y ATE.
    
    :param atd: Puntuación de Acciones Técnicas Dinámicas
    :param ate: Puntuación de Acciones Técnicas Estáticas
    :return: Puntuación del Factor de Frecuencia (FF)
    """
    return max(atd, ate)

def obtener_valor_ingresado(mensaje, valor_por_defecto=0):
    """
    Solicita al usuario ingresar un valor y valida la entrada.
    
    :param mensaje: Mensaje a mostrar al usuario
    :param valor_por_defecto: Valor a utilizar si no se ingresa ningún valor
    :return: Valor ingresado por el usuario
    """
    while True:
        try:
            entrada = input(mensaje)
            if entrada.strip() == '':
                return valor_por_defecto
            valor = float(entrada)
            if valor < 0:
                print("Por favor, ingrese un valor positivo.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número válido.")

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

    # Intentar extraer puntuaciones del JSON
    atd = data.get('AccionesTecnicasDinamicas', None)
    ate = data.get('AccionesTecnicasEstaticas', None)

    # Si no están presentes en el JSON, pedir al usuario que ingrese los valores
    if atd is None or ate is None:
        print("Algunos valores no se encontraron en el archivo JSON.")
        if atd is None:
            atd = obtener_valor_ingresado("Ingrese la puntuación de Acciones Técnicas Dinámicas (ATD): ")
        if ate is None:
            ate = obtener_valor_ingresado("Ingrese la puntuación de Acciones Técnicas Estáticas (ATE): ")

    # Calcular el FF
    ff = calcular_ff(atd, ate)

    # Añadir el cálculo al JSON
    data['FF'] = ff

    # Guardar el JSON actualizado
    updated_json_path = json_path.replace('.json', '__ff.json')
    with open(updated_json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

    print(f"El JSON se ha actualizado con el Factor de Frecuencia y guardado en {updated_json_path}.")

if __name__ == "__main__":
    main()
