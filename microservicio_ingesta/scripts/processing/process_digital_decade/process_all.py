from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import json

# Lista de códigos de sector NACE para iterar
LISTA_BREAKDOWNS_EMPRESA = [
    'c', 'e', 'f', 'g', 'h', 'i', 'ict', 'j', 'l68', 'm', 'n'
]

# Diccionario para mapear códigos NACE a nombres descriptivos
CODS_NACE = {
    'c': 'Manufacturing',
    'e': 'Water supply; sewerage, waste management and remediation activities',
    'f': 'Construction',
    'g': 'Wholesale and retail trade; repair of motor vehicles and motorcycles',
    'h': 'Transportation and storage',
    'i': 'Accommodation and food service activities',
    'ict': 'Information and Communication Technology - total',
    'j': 'Information and communication',
    'l68': 'Real estate activities',
    'm': 'Professional, scientific and technical activities',
    'n': 'Administrative and support service activities'
}
def obtener_anno_display(content):
    soup = BeautifulSoup(content, 'html.parser')

    period_label = soup.find('label', attrs={'for': 'period'})
    if period_label:
        parent_div = period_label.find_parent('div', class_='chart-filter')
        selected_filter_span = parent_div.select_one('div.multiselect__tags span')
        
        return int(selected_filter_span.text.strip())

def extraer_datos_de_html(content: str, cod_nace: str, nombre_resultado: str) -> pd.DataFrame:
    """
    Parsea el contenido HTML para extraer los datos del gráfico y los devuelve en un DataFrame.
    Si no hay datos, devuelve un DataFrame vacío.
    """
    if not content:
        # Si el contenido es None (porque Playwright falló o no encontró el gráfico),
        # devolvemos un DataFrame vacío con la estructura correcta.
        return pd.DataFrame(columns=['pais', nombre_resultado, 'sector'])

    soup = BeautifulSoup(content, 'html.parser')

    # Buscamos directamente las barras del gráfico que contienen la información en 'aria-label'
    grafico_paths = soup.select('g.highcharts-tracker path[aria-label]')
    
    if not grafico_paths:
        print(f"No se encontraron datos de gráfico para el sector {cod_nace}.")
        return pd.DataFrame(columns=['pais', nombre_resultado, 'sector'])

    datos_extraidos = [i.get('aria-label') for i in grafico_paths]

    resultado = {}
    for item in datos_extraidos:
        if ',' in item:
            partes = item.split(',', 1)
            # Limpiamos el nombre del país y el valor (quitando el punto y el %)
            pais = partes[0].strip()
            valor_str = partes[1].strip().rstrip('.%')
            resultado[pais] = valor_str

    if not resultado:
        return pd.DataFrame(columns=['pais', nombre_resultado, 'sector'])

    print(f"Datos extraídos para el sector {CODS_NACE.get(cod_nace, 'Desconocido')}: {len(resultado)} países.")
    
    df = pd.DataFrame(list(resultado.items()), columns=['pais', nombre_resultado])
    df['sector'] = CODS_NACE.get(cod_nace, 'Desconocido')
    df['periodo'] = obtener_anno_display(content)
    
    return df

def procesar_contents(ruta_crudos, ruta_filtered, nombre_resultado):
    """
    Orquesta el proceso de scraping para uno o varios sectores y guarda el resultado.
    """
    with open(ruta_crudos, 'r', encoding='utf-8') as f:
        json_contents = json.load(f)
    lista_dataframes = []
        # Iteramos sobre cada código de sector para las empresas
    for anno, cods_nace in json_contents.items():
        for cod_nace, content in cods_nace.items():
        # La función siempre devuelve un DF, aunque esté vacío, así que podemos añadirlo directamente.
            df_content = extraer_datos_de_html(content, cod_nace, nombre_resultado)
            if not df_content.empty:
                lista_dataframes.append(df_content)
                # else

    # --- SOLUCIÓN AL PROBLEMA DEL CONCAT ---
    # Si la lista de DataFrames no está vacía, los concatenamos.
    if lista_dataframes:
        df_final = pd.concat(lista_dataframes, ignore_index=True)
        # Eliminar filas donde el valor no sea numérico (por si acaso)
        df_final = df_final[pd.to_numeric(df_final[nombre_resultado], errors='coerce').notna()]
        df_final.to_csv(ruta_filtered, index=False)
        print(f"\nProceso completado. Datos guardados en: {ruta_filtered}")
        print(f"Total de registros guardados: {len(df_final)}")
    else:
        print("No se pudieron extraer datos para ningún sector. No se ha generado el archivo CSV.")


def process_data_digital_decade(ruta_crudos, ruta_filtered, nombre_resultado):
    procesar_contents(ruta_crudos, ruta_filtered, nombre_resultado)
