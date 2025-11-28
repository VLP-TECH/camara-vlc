import requests
from bs4 import BeautifulSoup
import os

# TODO ESTA EN DESUSO, SE PUEDE ELIMINAR
def obtener_url_archivo_actual(url, headers):

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        cajas = soup.find('body').find('div', class_='dialog-off-canvas-main-canvas').find('div', class_='main-container js-quickedit-main-content').find('div', class_='region region-content').find('div', class_='layout-cnmc-1col cnmc-layout').find('div', class_='region-main').find('div', class_='container').find('div', class_='row').find('div', class_='col-sm-12').find('div', class_='block-region-main').find_all('div', class_='block clearfix')[-1].find('div', class_='field field--name-body field--type-text-with-summary field--label-hidden field--item').find_all('div', class_='well')

        for i in cajas:
            info = i.find_all('p', recursive=False)[0].find('a')

            if info.find('span', class_='icon-zip-big').text.startswith('Últimas oleadas'):
                enlace = info.get('href')

    except Exception as e:
        print('Ha habido un error con la respuesta http')

    return enlace

def descargar_archivo_actual(enlace, carpeta_destino, headers, nombre_archivo=None):

    ruta_completa_archivo = os.path.join(carpeta_destino, nombre_archivo)

    try:
        with requests.get(enlace, stream=True, headers=headers) as r:
            r.raise_for_status()

            # Escribir el contenido del archivo en chunks
            with open(ruta_completa_archivo, 'wb') as f:
                # Leer en bloques de 8KB
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"Archivo descargado exitosamente en: {ruta_completa_archivo}")

    except requests.exceptions.RequestException as e:
        print(f'Error al descargar el archivo: {e}')
    except Exception as e:
        print(f'Ocurrió un error inesperado: {e}')

def download_panel_hogares(url, headers, ruta_destino, nombre_archivo):
    enlace = obtener_url_archivo_actual(url, headers)
    descargar_archivo_actual(enlace, ruta_destino, headers, nombre_archivo)