from pyaxis import pyaxis
import pandas as pd
import re

def limpiar_sector(sector_str):
    """
    Limpia la descripción del sector eliminando prefijos numéricos (con o sin puntos)
    y sufijos de CNAE.
    """
    if not isinstance(sector_str, str):
        return sector_str
    
    # --- LÍNEA MODIFICADA ---
    # La expresión ahora acepta prefijos como "2 Coquerias..." o "3 Metalurgia..."
    cleaned_str = re.sub(r'^\d+(\.\d+)*\.?\s*', '', sector_str)
    
    # El resto de la función no necesita cambios
    cleaned_str = re.sub(r'\s*\([\s\S]*\)$', '', cleaned_str)
    cleaned_str = cleaned_str.strip().strip('"')
    
    return cleaned_str

def limpiar_datos(df: pd.DataFrame, filtros: list, columnas: list, unidad_medida: str):
    for filtro, valor in filtros:
        df = df.loc[df[filtro] == valor]
    
    df_filtrado = df[columnas].copy()
    df_filtrado['pais'] = 'Spain'

    df_filtrado = df_filtrado.rename(columns={'DATA': unidad_medida})
    df_filtrado[unidad_medida] = pd.to_numeric(df_filtrado[unidad_medida])

    return df_filtrado


def renombrar_columnas(df: pd.DataFrame, cambios_nombre):
    diccionario_cambios = dict(cambios_nombre)
    df = df.rename(columns=diccionario_cambios)

    return df


def normalizar_periodo(df: pd.DataFrame):
    df = df.loc[df['periodo'].str.contains('enero', case=False)].copy()
    df['periodo'] = df['periodo'].str.split(' ').str[-1]

    df['periodo'] = df['periodo'].astype(int)
    df = df.loc[df['periodo'] >= 2015]

    return df


def process_data_ine(ruta_datos_crudos: str, ruta_datos_unfiltered: str, ruta_datos_filtered: str, columnas: list, filtros: list, cambios_nombre: list ,unidad_medida):
    archivo_px = pyaxis.parse(uri=str(ruta_datos_crudos), encoding='ISO-8859-1')

    columnas.append('DATA')
    df = pd.DataFrame(archivo_px['DATA'])
    df.to_csv(ruta_datos_unfiltered)
    # Para añadir nuevos datos de ine a la base de datos se añade aqui un exit y se pueden comprobar los nombres de las columnas
    # exit()

    df_filtrado = limpiar_datos(df, filtros, columnas, unidad_medida)

    if cambios_nombre:
        df_final = renombrar_columnas(df_filtrado, cambios_nombre)
    else:
        df_final = df_filtrado

    if 'periodo' in df_final.columns:
        try:
            df_final['periodo'] = df_final['periodo'].astype(int)

        except ValueError:
            print()
            df_final = normalizar_periodo(df_final)

    if 'provincia' in df_final.columns:
        df_final['provincia'] = df_final['provincia'].str.replace(r'^\d+\s+', '', regex=True)
        df_final['provincia'] = df_final['provincia'].str.split('/').str[0]

    if 'sector' in df_final.columns:
        df_final['sector'] = df_final['sector'].apply(limpiar_sector)

    df_final.to_csv(ruta_datos_filtered)