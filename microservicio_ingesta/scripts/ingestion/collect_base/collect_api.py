import json
import os
import requests

def fetch_eurostat_data(url):
    """
    Recopila datos de la API de Eurostat y los guarda en formato JSON.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() 
        json_completo = response.json()
        return json_completo
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de Eurostat: {e}")
        return None


def collect_data_api(url, nombre_archivo, ruta_datos_crudos):

    datos = fetch_eurostat_data(url)

    ruta_completa_destino = os.path.join(ruta_datos_crudos, nombre_archivo)

    if datos:

        with open(ruta_completa_destino, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        
        print(f'Datos guardados en la ruta: {ruta_completa_destino}')
    else:
        print(f'No se pudieron obtener los datos crudos de la api para la url {url}')


