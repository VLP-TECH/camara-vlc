from bs4 import BeautifulSoup
import requests
import os

def descargar_tabla_por_id(id, nombre_archivo: str, carpeta_destino: str, tipo_tabla: str):

    ruta_completa_destino = os.path.join(carpeta_destino, nombre_archivo)
    print(f'Comprobando que la carpeta {ruta_completa_destino} exita...')
    os.makedirs(carpeta_destino, exist_ok=True)
    url = f'https://ine.es/jaxiT3/files/{tipo_tabla}/es/px/{id}.px?nocab=1'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        with requests.get(url, stream=True, headers=headers) as respuesta:
            respuesta.raise_for_status()
            print("Descarga en progreso... guardando en archivo.")

            with open(ruta_completa_destino, 'wb') as archivo_local:
                for chunk in respuesta.iter_content(chunk_size=8192):
                    archivo_local.write(chunk)

        print('El archivo se ha descargado con éxito')
        
        return ruta_completa_destino

    except requests.exceptions.RequestException as e:
        print(f'No se pudo descargar el archivo: {e}')

