from data.processed.indicadores.roles import CATALOGO_ROLES
import pandas as pd
from database.modelos.dimensiones import Dimension
from database.modelos.subdimensiones import Subdimension
from database.modelos.definicion_indicadores import DefinicionIndicador
from database.modelos.componentes_indicadores import ComponenteIndicador
from database.modelos.datos_crudos import DatoCrudo
from database.modelos.datos_macro import DatoMacro
from database.modelos.resultados_indicadores import ResultadoIndicador
from database.connection import SessionLocal
import logging
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def asegurar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    columnas_requeridas = ['periodo', 'pais', 'provincia', 'tamano_empresa', 'sector']
    df_copy = df.copy()

    for col in columnas_requeridas:
        if col not in df_copy.columns:
            df_copy[col] = None
            logging.info(f"Columna '{col}' no encontrada en el CSV. Añadida con valores nulos.")

    return df_copy

def obtener_claves_existentes(session, model, indicador_id, dato):
    columnas_clave = [
        model.periodo,
        model.pais,
        model.provincia,
        model.tamano_empresa,
        model.sector
    ]

    if dato['procesado']:
        query = session.query(*columnas_clave).filter(model.id_indicador == indicador_id)
    else:
        query = session.query(*columnas_clave).filter(model.descripcion_dato == dato['descripcion_dato'])

    claves_existentes = {tuple(row) for row in query.all()}

    return claves_existentes


def obtener_id_indicador(session, dato):
    query = session.query(DefinicionIndicador).join(ComponenteIndicador, DefinicionIndicador.id == ComponenteIndicador.id_indicador).filter(ComponenteIndicador.descripcion_dato == dato['descripcion_dato'])
    indicador = query.first()

    if not indicador:
        query = session.query(DefinicionIndicador).filter(DefinicionIndicador.nombre == dato['nombre_indicador'])
        indicador = query.first()
    
    return indicador.id


def insertar_datos(df: pd.DataFrame, dato:dict, session, model):

    df_original = asegurar_columnas(df)
    indicador_id = obtener_id_indicador(session, dato) if model == DatoCrudo else None

    if model == DatoCrudo and not dato['procesado'] and indicador_id is None:
        logging.warning(f"No se encontró indicador para '{dato.get('descripcion_dato')}'. Saltando inserción.")
        return

    claves_existentes = obtener_claves_existentes(session, model, indicador_id, dato)

    if not claves_existentes:
        df_nuevos = df_original
    else:
        columnas_clave_df = ['periodo', 'pais', 'provincia', 'tamano_empresa', 'sector']

        df_original['clave_temp'] = list(zip(
            *(df_original[c].fillna('nan').astype(str) for c in columnas_clave_df)
        ))

        claves_existentes_str = {
            tuple(str(item) if item is not None else 'nan' for item in key)
            for key in claves_existentes
        }
        df_nuevos = df_original[~df_original['clave_temp'].isin(claves_existentes_str)].copy()
        df_nuevos.drop(columns=['clave_temp'], inplace=True)
    nuevos_datos = []

    base_args = {
        'descripcion_dato': dato.get('descripcion_dato'),
        'unidad': dato['nombre_resultado']
    }

    if model == DatoCrudo:
        base_args['id_indicador'] = indicador_id
        base_args['procesado'] = dato['procesado']

    for _, row in df_nuevos.iterrows():
        row_data = row.to_dict()
        nuevo_dato = model(
            **base_args,
            valor=row_data.get(dato['nombre_resultado']),
            provincia=row_data.get('provincia'),
            pais=row_data.get('pais'),
            periodo=row_data.get('periodo'),
            tamano_empresa=row_data.get('tamano_empresa'),
            sector=row_data.get('sector')
        )
            
        nuevos_datos.append(nuevo_dato)

    if nuevos_datos:
        session.add_all(nuevos_datos)
        descripcion_final = dato.get('descripcion_dato') or dato.get('nombre_indicador')
        logging.info(f'Éxito: {len(nuevos_datos)} nuevos registros para "{descripcion_final}" preparados para inserción.')


def loading():
    session = SessionLocal()
    try:
        todas_las_descripciones = [
            componente['descripcion_dato']
            for indicador in CATALOGO_ROLES
            for componente in indicador['componentes']
            if componente['descripcion_dato'] != 'nan'
        ]

        conteo_descripciones = Counter(todas_las_descripciones)

        datos_macro = [
            descripcion
            for descripcion, conteo in conteo_descripciones.items()
            if conteo > 1
        ]

        from database.guia_datos import GUIA_DATOS_PROCESADOS
        
        for dato in GUIA_DATOS_PROCESADOS:
            if dato['procesado'] == False and dato['descripcion_dato'] == None:
                continue

            try:
                df = pd.read_csv(dato['ruta_archivo'])

            except FileNotFoundError:
                logging.error(f"Archivo no encontrado, saltando: {dato['ruta_archivo']}")
                continue 

            except Exception as e:
                logging.error(f"Error al leer el CSV {dato['ruta_archivo']}: {e}")
                continue

            try:
                modelo = DatoMacro if dato.get('descripcion_dato') in datos_macro else DatoCrudo
                insertar_datos(df, dato, session, modelo)

                session.commit()
                print('SE HACE COMMMIT')
            except Exception as e:
                logging.error(f"Fallo al procesar los datos del archivo {dato['ruta_archivo']}. Revirtiendo cambios para este archivo. Error: {e}")
                session.rollback()
    finally:
        logging.info("Proceso de iteración finalizado. Cerrando sesión.")
        session.close()
        
if __name__ == '__main__':
    loading()