from modelos.models import Processor_ine as Processor
from data.processed.indicadores.indicators import CATALOGO_COMPLETO

DATOS = [
        Processor(
                nombre_archivo='poblacion_por_provincia',
                nombre_resultado='poblacion',
                columnas=['Provincias', 'Periodo'],
                filtros=[
                        ['Edad simple', 'Todas las edades'],
                        ['Sexo', 'Total']
                ],
                cambios_nombre=[
                        ['Periodo', 'periodo'],
                        ['Provincias', 'provincia']
                ],
                descripcion_dato='Población total'
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Teletrabajo'],
            nombre_archivo = 'empresas_permiten_teletrabajo',
            nombre_resultado = '%(empresas)',
            columnas = ['Principales variables', 'Agrupación de actividad (excepto CNAE 56, 64-66 y 95.1)', 'Tamaño de la empresa'],
            filtros = [
                    ['Principales variables', 'D.10 % de empresas que permiten la realización de teletrabajo por parte de sus empleados']
                ],
            cambios_nombre = [
                    ['Agrupación de actividad (excepto CNAE 56, 64-66 y 95.1)', 'sector'],
                    ['Tamaño de la empresa', 'tamano_empresa']
            ],
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Empresas con infraestructura en la nube'],
            nombre_archivo = 'empresas_servicios_cloud_computing',
            nombre_resultado = '%(empresas)',
            columnas = ['Principales variables', 'Agrupación de actividad (excepto CNAE 56, 64-66 y 95.1)', 'Tamaño de la empresa'],
            filtros = [
                    ['Principales variables', 'F.1 % de empresas que compran servicios de cloud computing (1)']
                ],
            cambios_nombre = [
                    ['Agrupación de actividad (excepto CNAE 56, 64-66 y 95.1)', 'sector'],
                    ['Tamaño de la empresa', 'tamano_empresa']
            ],
            procesado=True
        ),
        Processor(
            indicador = CATALOGO_COMPLETO['Número de empresas que realizan I+D en el sector TIC'],
            nombre_archivo = 'empresas_tic_actividades_i+d',
            nombre_resultado = 'nº(empresas)',
            columnas = ['Tipo de indicador', 'Periodo de referencia'],
            filtros = [
                    ['Tipo de indicador', 'Número de empresas que realizan I+D'],
                    ['Rama de actividad', 'TOTAL SECTOR TIC']
                ],
            cambios_nombre = [
                    ['Periodo de referencia', 'periodo']
            ],
            procesado=True
        )
    ]

def processor_ine():
    datos_insercion = []
    for dato in DATOS:
        datos_insercion.append(dato.procesar())

    return datos_insercion