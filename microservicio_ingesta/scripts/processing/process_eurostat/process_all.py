import json
from .SMDX_inverso import invertir_decodificacion_sdmx
import pandas as pd
import numpy as np
import datetime
from pathlib import Path

def formateo_quarterly(df_cuatrimestral, nombre_resultado):
    df_cuatrimestral['periodo'] = df_cuatrimestral['periodo'].str[:-3]
    anno_actual = datetime.date.today().year

    # Elimino el año actual, dado que al brindar datos cuatrimestrales, el año actual no va a reflejar los datos correctamente
    df = df_cuatrimestral.groupby(['pais', 'periodo'])[nombre_resultado].sum().reset_index()
    df['periodo'] = pd.to_numeric(df['periodo'])

    df = df.loc[df['periodo'] != anno_actual]

    return df

def filtrar_periodo_reciente(df: pd.DataFrame, nombre_resultado):
    '''
    Función encargada de filtrar por el último año del cual hay datos registrados
    y guardar solo los datos solicitados, a la vez que agrupando los diferentes grupos de resultados en uno solo
    '''
    # Compruebo si la frecuencia de datos es cuatrimestral
    if 'freq' in df.columns and (df['freq'] == 'Quarterly').any():
        df = formateo_quarterly(df, nombre_resultado)
    
    df['periodo'] = df['periodo'].astype(int)

    df_final = df.loc[df['periodo'] >= 2015]

    return df_final

def nombrar_columnas(df: pd.DataFrame, nombre_resultado) -> pd.DataFrame:
    return df.rename(columns={'geo': 'pais', 'resultado': nombre_resultado, 'time': 'periodo', 'nace_r2': 'sector', 'size_emp': 'tamano_empresa', 'ind_type': 'Grupo Edad'})

def media_ponderada(x, nombre_resultado):
    suma_pesos = x['poblacion'].sum()
    
    if suma_pesos == 0:
        # Si la población total para este grupo es 0, no podemos calcular la media.
        # Devolvemos 0 como resultado.
        return 0

    else:
        # Si la población es mayor que 0, calculamos la media ponderada de forma normal.
        return round(np.average(x[nombre_resultado], weights=x['poblacion']), 2)


def limpiar_datos(df: pd.DataFrame, df_poblacion_pais_y_franja: pd.DataFrame, nombre_resultado) -> pd.DataFrame:
    """
    Calcula la media ponderada de un indicador para todos los periodos comunes
    entre el DataFrame del indicador y el de la población.

    Args:
        df: DataFrame con los datos del indicador (ej: % uso de internet),
            debe tener las columnas 'ind_type', 'pais' y 'periodo'.
        df_poblacion_pais_y_franja: DataFrame con los datos de población por franjas,
            debe tener las columnas 'Grupo Edad', 'pais', 'periodo' y 'poblacion'.

    Returns:
        Un DataFrame con el resultado de la media ponderada para cada país y periodo.
    """
    df['periodo'] = df['periodo'].astype(str)
    df_poblacion_pais_y_franja['periodo'] = df_poblacion_pais_y_franja['periodo'].astype(str)

    merged_df = pd.merge(df, df_poblacion_pais_y_franja, on=['pais', 'Grupo Edad', 'periodo'])

    resultados = merged_df.groupby(['pais', 'periodo']).apply(
        media_ponderada,
        nombre_resultado=nombre_resultado
    )

    resultados_df = resultados.reset_index(name=nombre_resultado)

    return resultados_df

def agrupar_por_franjas(df: pd.DataFrame) -> pd.DataFrame:

    bins = [15, 24, 64, 74] 

    labels = ['Individuals, 16 to 24 years old', 'Individuals, 25 to 64 years old', 'Individuals, 65 to 74 years old']
    df['Grupo Edad'] = pd.cut(
        x=df['age'].astype(int),
        bins=bins,
        labels=labels,
        right=True
    )
    df['poblacion'] = df['poblacion'].astype(int)

    df_agrupado = df.groupby(['pais', 'Grupo Edad', 'periodo'], observed=True)['poblacion'].sum().reset_index()
    return df_agrupado

def leer_archivo_a_df(ruta_datos_crudos, ruta_datos_unfiltered):
    try:

        with open(ruta_datos_crudos, 'r', encoding='utf-8') as f:
            datos_crudos = json.load(f)

    except FileNotFoundError:
        print(f'No se ha encontrado el archivo con los datos crudos en la ruta: {ruta_datos_crudos}')
        return

    lista_resultados = invertir_decodificacion_sdmx(datos_crudos)

    with open(ruta_datos_unfiltered, 'w', encoding='utf-8') as f:
        json.dump(lista_resultados, f, indent=4, ensure_ascii=False)

    return pd.DataFrame(lista_resultados)


def process_data_poblacion_por_edad(ruta_datos_crudos, ruta_datos_unfiltered, ruta_datos_filtered, nombre_resultado):

    df = leer_archivo_a_df(ruta_datos_crudos, ruta_datos_unfiltered)

    df_actual = nombrar_columnas(df, nombre_resultado)

    df_filtrado = df_actual[['pais', nombre_resultado, 'periodo', 'age']].copy()
    df_filtrado['age'] = df_filtrado['age'].str.split(' ').str[0]
    df_filtrado = agrupar_por_franjas(df_filtrado)

    df_final = filtrar_periodo_reciente(df_filtrado, nombre_resultado)

    df_final.to_csv(ruta_datos_filtered)


def process_data_eurostat(ruta_datos_crudos, ruta_datos_unfiltered, ruta_datos_filtered, nombre_resultado):
    COLUMNAS = ['pais', nombre_resultado, 'periodo', 'sector', 'tamano_empresa']

    df = leer_archivo_a_df(ruta_datos_crudos, ruta_datos_unfiltered)

    df_actual = nombrar_columnas(df, nombre_resultado)
    df_actual = filtrar_periodo_reciente(df_actual, nombre_resultado)

    if 'unit' in df_actual.columns and (df_actual['unit'] == 'Percentage of individuals').any():
        ruta_csv_edades = Path("data") / "processed" / "eurostat" / "filtered" / "crudo" / "poblacion_por_pais_y_edad.csv"
        df_poblacion_franjas = pd.read_csv(ruta_csv_edades)

        df_actual = limpiar_datos(df_actual, df_poblacion_franjas, nombre_resultado)

    columnas_a_seleccionar = [col for col in COLUMNAS if col in df_actual.columns]
    df_final = df_actual[columnas_a_seleccionar]
    
    df_final = df_final.loc[~df_final['pais'].str.contains('Euro', case=False, na=False)]

    df_final.to_csv(ruta_datos_filtered)