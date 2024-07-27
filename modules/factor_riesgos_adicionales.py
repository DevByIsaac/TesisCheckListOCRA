import json
import os
import glob

def calculate_additional_risks(json_data):
    """
    Calcula el Factor de Riesgos Adicionales (FC) basado en los riesgos adicionales del JSON proporcionado.
    
    :param json_data: Diccionario con datos de riesgos adicionales
    :return: Puntuación del Factor de Riesgos Adicionales (FC)
    """
    # Definir criterios para calcular el FC
    # Ejemplo: Puedes tener varios campos que influyen en el FC
    riesgo_adicional_1 = json_data.get('RiesgoAdicional1', 2)
    riesgo_adicional_2 = json_data.get('RiesgoAdicional2', 3)
    
    # Ejemplo de fórmula para el FC
    fc = riesgo_adicional_1 * 0.5 + riesgo_adicional_2 * 0.3
    
    return fc

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

    # Calcular el FC
    fc = calculate_additional_risks(data)

    # Añadir el cálculo al JSON
    data['Factor de Riesgos Adicionales'] = fc

    # Guardar el JSON actualizado
    updated_json_path = json_path.replace('.json', '_fc.json')
    with open(updated_json_path, 'w') as file:
        json.dump(data_list, file, indent=4)

    print(f"El JSON se ha actualizado con el Factor de Riesgos Adicionales (FC) y guardado en {updated_json_path}.")

if __name__ == "__main__":
    main()