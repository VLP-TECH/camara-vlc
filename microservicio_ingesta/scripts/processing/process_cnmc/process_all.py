import pandas as pd
import json
from pathlib import Path

RUTA_LINEAS_BANDA_ANCHA_TOTAL = 'total_suscripciones_banda_ancha.csv'


def crear_total_nacional(df, ruta_entrada, columna_a_sumar, nombre_archivo_salida):
    """
    Función genérica que lee datos agrupados (ej: por provincia),
    los unifica a nivel nacional y los guarda en un archivo específico.
    """
    columna_periodo = 'periodo' if 'periodo' in df.columns else 'anno'
    
    df_nacional = df.groupby(columna_periodo)[columna_a_sumar].sum().reset_index()

    ruta_salida = ruta_entrada.parent / nombre_archivo_salida
    df_nacional.to_csv(ruta_salida, index=False)
    print(f"ÉXITO: Total nacional guardado en '{ruta_salida.name}'.")

def calcular_coste_mensual(df: pd.DataFrame, ruta_salida, archivo_datos_totales, unidades):
    ruta_datos_totales = ruta_salida.parent / archivo_datos_totales
    df_totales = pd.read_csv(ruta_datos_totales)

    df_coste_mensual = pd.merge(
        df,
        df_totales,
        on='periodo',
        how='inner'
    )

    df_coste_mensual['coste_mensual_euros'] = df_coste_mensual[unidades] / df_coste_mensual['lineas_o_accesos']
    df_coste_mensual['coste_mensual_euros'] = round(df_coste_mensual['coste_mensual_euros'], 2)

    del df_coste_mensual[unidades]

    df_coste_mensual = df_coste_mensual.rename(columns={'coste_mensual_euros': unidades})

    return df_coste_mensual


def carga_y_procesamiento(ruta_datos_crudos, filtro, ruta_datos_unfiltered, agrupaciones, unidades):
    with open(ruta_datos_crudos, 'r', encoding='utf-8') as f:
        datos_crudos = json.load(f)

    datos_crudos = datos_crudos['result']['records']

    df = pd.DataFrame(datos_crudos)

    medida = df['unidades']

    df['anno'] = df['anno'].astype(int)
    
    df_filtrado = df.loc[df[filtro[0]] == filtro[1]]

    df_filtrado.to_csv(ruta_datos_unfiltered)
    df_filtrado = df_filtrado.groupby(agrupaciones)[unidades].sum().reset_index()
    
    df_final = df_filtrado.loc[df_filtrado['anno'] > 2014]

    return df_final, medida

def comprobacion_unidades(df_final, medida, unidades):
    if (medida == 'Millones de euros').any():
        df_final[unidades] = round((df_final[unidades] * 1000000) / 12, 2)

    return df_final

def process_data_cnmc(ruta_datos_crudos, ruta_datos_unfiltered, ruta_datos_filtered, filtro, agrupaciones, unidades):

    df_final, medida = carga_y_procesamiento(ruta_datos_crudos, filtro, ruta_datos_unfiltered, agrupaciones, unidades)
    
    df_final = comprobacion_unidades(df_final, medida, unidades)

    df_final = df_final.rename(columns={'anno': 'periodo'})

    df_final['pais'] = 'España'

    if 'provincia' in agrupaciones:
        if filtro[1] == 'Banda ancha fija' and filtro[0] == 'servicio':
            crear_total_nacional(
                df=df_final,
                ruta_entrada=ruta_datos_filtered,
                columna_a_sumar='lineas_o_accesos',
                nombre_archivo_salida=RUTA_LINEAS_BANDA_ANCHA_TOTAL
            )


    df_final.to_csv(ruta_datos_filtered)

def calcular_precio_mensual_cnmc(ruta_datos_crudos, ruta_datos_unfiltered, ruta_datos_filtered, filtro, agrupaciones, unidades):
    # process_data_cnmc(ruta_datos_crudos, ruta_datos_unfiltered, ruta_datos_filtered, filtro, agrupaciones, unidades)

    df_final, medida = carga_y_procesamiento(ruta_datos_crudos, filtro, ruta_datos_unfiltered, agrupaciones, unidades)
    df_final = comprobacion_unidades(df_final, medida, unidades)

    df_final = df_final.rename(columns={'anno': 'periodo'})

    df_final['pais'] = 'España'

    df_calculado = calcular_coste_mensual(
        df=df_final,
        ruta_salida=ruta_datos_filtered,
        archivo_datos_totales=RUTA_LINEAS_BANDA_ANCHA_TOTAL,
        unidades=unidades
    )

    df_calculado.to_csv(ruta_datos_filtered)