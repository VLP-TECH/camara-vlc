from .connection import Base, engine, SessionLocal
from database.modelos.definicion_indicadores import DefinicionIndicador
from database.modelos.dimensiones import Dimension as DimensionModel
from database.modelos.subdimensiones import Subdimension as SubdimensionModel
from database.modelos.definicion_indicadores import DefinicionIndicador as IndicadorModel
from database.modelos.componentes_indicadores import ComponenteIndicador as ComponenteModel
from database.modelos.datos_crudos import DatoCrudo
from database.modelos.resultados_indicadores import ResultadoIndicador
from database.modelos.datos_macro import DatoMacro
from modelos.models import Dimension, Subdimension
from data.processed.indicadores.indicators import CATALOGO_COMPLETO
from data.processed.indicadores.formulas import CATALOGO_OPERACIONES
from data.processed.indicadores.roles import CATALOGO_ROLES
from modelos.models import RolDato as RolDatoEnum
from collections import Counter
from data.processed.indicadores.indicators import CATALOGO_COMPLETO
from sqlalchemy import text


DATOS_ESG = {
    Dimension.EMPRENDIMIENTO_E_INNOVACION: {
        'peso': 10,
        'subdimensiones': [
            {'nombre': Subdimension.ACCESO_FINANCIACION, 'peso': 0},
            {'nombre': Subdimension.DINAMISMO_EMPRENDEDOR, 'peso': 0},
            {'nombre': Subdimension.INFRAESTRUCTURA_APOYO, 'peso': 0},
            {'nombre': Subdimension.POLITICAS_FOMENTO, 'peso': 0}
        ]
    },
    Dimension.CAPITAL_HUMANO: {
        'peso': 20,
        'subdimensiones': [
            {'nombre': Subdimension.COMPETENCIAS_DIGITALES, 'peso': 0},
            {'nombre': Subdimension.FORMACION_CONTINUA, 'peso': 0},
            {'nombre': Subdimension.TALENTO_PROFESIONAL, 'peso': 0}
        ]
    },
    Dimension.ECOSISTEMA_Y_COLABORACION: {
        'peso': 15,
        'subdimensiones': [
            {'nombre': Subdimension.ATRACTIVO_ECOSISTEMA, 'peso': 0},
            {'nombre': Subdimension.PROVISION_TECNOLOGICA, 'peso': 0},
            {'nombre': Subdimension.TRANSFERENCIA_CONOCIMIENTO, 'peso': 0}
        ]
    },
    Dimension.INFRAESTRUCTURA_DIGITAL: {
        'peso': 15,
        'subdimensiones': [
            {'nombre': Subdimension.ACCESO_INFRAESTRUCTURAS, 'peso': 0}
        ]
    },
    Dimension.SERVICIOS_PUBLICOS_DIGITALES: {
        'peso': 10,
        'subdimensiones': [
            {'nombre': Subdimension.DISPONIBILIDAD_SERVICIOS_DIGITALES, 'peso': 0},
            {'nombre': Subdimension.INTEGRACION_ADMINISTRACION, 'peso': 0}
        ]
    },
    Dimension.SOSTENIBILIDAD_DIGITAL: {
        'peso': 5,
        'subdimensiones': [
            {'nombre': Subdimension.ECONOMIA_CIRCULAR, 'peso': 0},
            {'nombre': Subdimension.HUELLA_AMBIENTAL, 'peso': 0}
        ]
    },
    Dimension.TRANSFORMACION_DIGITAL: {
        'peso': 30,
        'subdimensiones': [
            {'nombre': Subdimension.ORGANIZACION_DIGITAL, 'peso': 0},
            {'nombre': Subdimension.DIGITALIZACION_BASICA, 'peso': 0},
            {'nombre': Subdimension.E_COMMERCE, 'peso': 0},
            {'nombre': Subdimension.TECNOLOGIAS_AVANZADAS, 'peso': 0}
        ]
    }
}

def reset_database():
    """Borra todas las tablas y las vuelve a crear usando CASCADE para robustez."""
    
    print("--- Borrando todas las tablas existentes (modo CASCADE) ---")
    
    with engine.connect() as connection:
        with connection.begin() as transaction:
            try:
                # Itera sobre las tablas en orden inverso para eliminar dependencias primero
                for table in reversed(Base.metadata.sorted_tables):
                    # Ejecuta el comando DROP TABLE con CASCADE
                    connection.execute(text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE;'))
            except Exception as e:
                print(f"Ocurrió un error al borrar las tablas: {e}")
                # El 'rollback' es automático si ocurre una excepción dentro del 'with'
                raise # Opcional: vuelve a lanzar el error si quieres que el script se detenga
                
    print("Éxito. Tablas borradas.")
    
    print("--- Creando todas las tablas de nuevo ---")
    Base.metadata.create_all(bind=engine)
    print("Éxito. Tablas creadas.")

def create_tables():
    """Crea todas las tablas definidas en los modelos."""
    print("Creando todas las tablas en la base de datos...")
    # Esta es la línea que físicamente crea las tablas
    Base.metadata.create_all(bind=engine)
    print("Éxito. Tablas creadas (o ya existían).")

def seed_data(lista_indicadores):
    db = SessionLocal()
    try:
        if db.query(DimensionModel).first():
            print('Los datos semilla ya existen, no se realizará ninguna acción')
            return
        
        todas_las_descripciones = [
            componente['descripcion_dato']
            for indicador in CATALOGO_ROLES
            for componente in indicador['componentes']
            if componente['descripcion_dato'] != 'nan'
        ]

        # Contar la frecuencia de cada descripción.
        conteo_descripciones = Counter(todas_las_descripciones)

        # Filtrar para quedarse solo con las descripciones que aparecen más de una vez.
        datos_macro = [
            descripcion
            for descripcion, conteo in conteo_descripciones.items()
            if conteo > 1
        ]

        dimensiones_a_crear = [
            DimensionModel(
                nombre=nombre_dim.value,
                peso=datos_dim['peso'],
                subdimensiones=[
                    SubdimensionModel(
                        nombre=datos_sub['nombre'].value,
                        peso=datos_sub['peso'],
                        indicadores=[
                            IndicadorModel(
                                nombre=indicador['nombre'],
                                origen_indicador=indicador['origen'],
                                formula= indicador['formula'],
                                importancia=indicador['importancia'],
                                fuente=indicador['fuente'],
                                componentes=[
                                    ComponenteModel(
                                        descripcion_dato=datos_comp['descripcion_dato'],
                                        fuente='DATOS_MACRO' if datos_comp['descripcion_dato'] in datos_macro else 'DATOS_CRUDOS',
                                        rol=datos_comp['rol']
                                    )
                                    for rol_info in CATALOGO_ROLES if rol_info['nombre_indicador'] == indicador['nombre'] 
                                    for datos_comp in rol_info['componentes']
                                ]
                            )
                            for indicador in lista_indicadores if indicador['subdimension'] == datos_sub['nombre'].value
                        ]
                        )
                    for datos_sub in datos_dim['subdimensiones']
                ]
            )
            for nombre_dim, datos_dim in DATOS_ESG.items()
        ]

        db.add_all(dimensiones_a_crear)

        db.commit()
        print('Semilla poblada con éxito')

    finally:
        db.close()

def fusionar_datos():
    operaciones_map = {item['nombre']: item['operacion'] for item in CATALOGO_OPERACIONES}

    # Construir la lista final de datos para la inserción
    datos_para_insertar = []
    for nombre, indicador_obj in CATALOGO_COMPLETO.items():
        # Busca la operación en el mapa. Si no la encuentra, usa un valor por defecto.
        operacion = operaciones_map.get(nombre, 'AGREGACION_DIRECTA')

        # Crea un diccionario con todos los datos necesarios para tu tabla
        datos_completos = {
            'nombre': indicador_obj.nombre,
            'dimension': indicador_obj.dimension.value,
            'subdimension': indicador_obj.subdimension.value,
            'origen': indicador_obj.origen,
            'importancia': indicador_obj.importancia,
            'fuente': indicador_obj.fuente,
            'formula': operacion
        }

        datos_para_insertar.append(datos_completos)


    return datos_para_insertar
    
    # poblar_indicadores_y_componentes(datos_para_insertar)

if __name__ == '__main__':
    reset_database()
    create_tables()
    seed_data(fusionar_datos())    