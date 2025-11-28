import zipfile
import os

def obtener_ultima_carpeta(direccion):
    if not os.path.isdir(direccion):
        print(f"Error: El directorio '{direccion}' no existe.")
        return None
    
    try:
        nombres_carpetas = []
        for nombre_item in os.listdir(direccion):
            ruta_completa_item = os.path.join(direccion, nombre_item)
            if os.path.isdir(ruta_completa_item):
                nombres_carpetas.append(nombre_item)

        oleada_max = 0

        nombre_ultima_carpeta = ''
        for i in nombres_carpetas:
            num_oleada = i.split('_')[1]
            if int(num_oleada) > oleada_max:
                nombre_ultima_carpeta = i
                oleada_max = int(num_oleada)

        return os.path.join(direccion, nombre_ultima_carpeta)
        

    except Exception as e:
        print(f'Ocurrió un error al leer el directorio: {e}')
        return None

def descomprimir_archivo(ruta_archivo_zip, carpeta_destino):

    try:
        with zipfile.ZipFile(ruta_archivo_zip, 'r') as zip:
            zip.extractall(carpeta_destino)
        
        print('Se descomprimió correctamente')

    except zipfile.BadZipFile:
        print(f'Error: El archivo {ruta_archivo_zip} no es un archivo ZIP valido')
    except Exception as e:
        print(f'Ocurrió un error inesperado al descomprimir {e}')